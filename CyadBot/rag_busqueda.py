# ---------------------------------------------------------------
# Módulo: rag_busqueda.py (VERSIÓN AUTO-INICIALIZABLE)
# ---------------------------------------------------------------

import chromadb
from sentence_transformers import SentenceTransformer
import os
import pickle
from typing import List, Dict, Optional
import hashlib

class RAGBuscador:
    def __init__(self, persist_directory: str = "./chroma_db", documentos_path: str = "./static/documentos"):
        print("🔄 Inicializando RAGBuscador...")
        
        self.persist_directory = persist_directory
        self.documentos_path = documentos_path
        self.chunks_file = os.path.join(persist_directory, "chunks.pkl")
        self.processed_files_file = os.path.join(persist_directory, "processed_files.pkl")
        
        # 1. Cargar modelo de embeddings
        print("🧠 Cargando modelo de embeddings...")
        self.model = SentenceTransformer(
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        )
        print("✅ Modelo de embeddings cargado")
        
        # 2. Configurar ChromaDB
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # 3. Verificar/Crear colección
        try:
            self.collection = self.client.get_collection("documentos_cyad")
            print("✅ Colección existente cargada")
        except:
            print("📁 Creando nueva colección...")
            self.collection = self.client.create_collection(
                name="documentos_cyad",
                metadata={"description": "Documentos académicos CyAD"}
            )
            print("✅ Nueva colección creada")
        
        # 4. Cargar registro de archivos procesados
        self.processed_files = self._cargar_archivos_procesados()
        
        # 5. ✅ AUTO-INDEXACIÓN: Si no hay documentos, indexar automáticamente
        if self.collection.count() == 0 and os.path.exists(self.documentos_path):
            print("🆕 No hay documentos indexados. Ejecutando auto-indexación...")
            self.indexar_documentos()
        elif self.collection.count() == 0:
            print("⚠️ No hay documentos indexados y no se encontró la ruta de documentos")
        else:
            print(f"📚 Colección lista con {self.collection.count()} chunks")
            print(f"📄 Archivos procesados: {len(self.processed_files)}")
    
    def _cargar_archivos_procesados(self) -> set:
        """Carga el registro de archivos ya procesados"""
        try:
            with open(self.processed_files_file, 'rb') as f:
                return set(pickle.load(f))
        except:
            return set()
    
    def _guardar_archivos_procesados(self):
        """Guarda el registro de archivos procesados"""
        os.makedirs(self.persist_directory, exist_ok=True)
        with open(self.processed_files_file, 'wb') as f:
            pickle.dump(list(self.processed_files), f)
    
    def _calcular_hash_archivo(self, file_path: str) -> str:
        """Calcula hash MD5 para detectar cambios"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    # ------------------------------------------------------------------
    # Indexar documentos (modo INCREMENTAL)
    # ------------------------------------------------------------------
    def indexar_documentos(self, forzar_reindexar: bool = False):
        """Indexa documentos desde la ruta configurada"""
        print(f"📂 Indexando documentos desde: {self.documentos_path}")
        
        if not os.path.exists(self.documentos_path):
            print(f"❌ Directorio no encontrado: {self.documentos_path}")
            return False
        
        # Buscar archivos TXT
        txt_files = [f for f in os.listdir(self.documentos_path) if f.endswith('.txt')]
        if not txt_files:
            print("❌ No se encontraron archivos .txt")
            return False
        
        print(f"📄 Encontrados {len(txt_files)} archivos TXT")
        
        # Filtrar archivos no procesados o modificados
        archivos_a_procesar = []
        
        for txt_file in txt_files:
            file_path = os.path.join(self.documentos_path, txt_file)
            file_hash = self._calcular_hash_archivo(file_path)
            file_id = f"{txt_file}_{file_hash}"
            
            if forzar_reindexar or file_id not in self.processed_files:
                archivos_a_procesar.append((txt_file, file_path, file_id))
            else:
                print(f"✅ {txt_file} - Ya indexado")
        
        if not archivos_a_procesar:
            print("🎉 Todos los archivos ya están indexados")
            return True
        
        print(f"🆕 Archivos a indexar: {len(archivos_a_procesar)}")
        
        all_chunks = []
        all_metadata = []
        nuevos_archivos_ids = []
        
        for txt_file, file_path, file_id in archivos_a_procesar:
            print(f"📖 Procesando: {txt_file}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                chunks = self._dividir_en_chunks(contenido, file_path)
                all_chunks.extend(chunks)
                all_metadata.extend([{"fuente": txt_file, "file_id": file_id}] * len(chunks))
                nuevos_archivos_ids.append(file_id)
                
                print(f"   ✅ {len(chunks)} chunks creados")
                
            except Exception as e:
                print(f"   ❌ Error procesando {txt_file}: {e}")
        
        if not all_chunks:
            print("❌ No se pudieron procesar chunks")
            return False
        
        # Generar embeddings y guardar
        print("🧮 Generando embeddings...")
        embeddings = self.model.encode(all_chunks).tolist()
        
        chunk_ids = [f"chunk_{self.collection.count() + i}" for i in range(len(all_chunks))]
        
        print("💾 Guardando en ChromaDB...")
        self.collection.add(
            embeddings=embeddings,
            documents=all_chunks,
            metadatas=all_metadata,
            ids=chunk_ids
        )
        
        # Actualizar registro
        self.processed_files.update(nuevos_archivos_ids)
        self._guardar_archivos_procesados()
        
        print(f"🎉 Indexación completada: {len(all_chunks)} chunks nuevos")
        print(f"📊 Total en base de datos: {self.collection.count()} chunks")
        return True
    
    # ------------------------------------------------------------------
    # Búsqueda principal
    # ------------------------------------------------------------------
    def buscar_contexto(self, pregunta: str, n_resultados: int = 3) -> Optional[str]:
        """Busca el contexto más relevante para una pregunta"""
        if self.collection.count() == 0:
            print("⚠️ No hay documentos indexados")
            return None
        
        try:
            pregunta_embedding = self.model.encode([pregunta]).tolist()
            
            resultados = self.collection.query(
                query_embeddings=pregunta_embedding,
                n_results=n_resultados
            )
            
            if not resultados['documents'] or not resultados['documents'][0]:
                return None
            
            documentos = resultados['documents'][0]
            distancias = resultados['distances'][0]
            
            contexto_relevante = []
            for doc, distancia in zip(documentos, distancias):
                if distancia < 1.0:
                    contexto_relevante.append(doc)
            
            if not contexto_relevante:
                return None
            
            contexto_completo = "\n\n".join(contexto_relevante)
            return self._limpiar_contexto(contexto_completo)
            
        except Exception as e:
            print(f"❌ Error en búsqueda RAG: {e}")
            return None
    
    # ------------------------------------------------------------------
    # Métodos auxiliares
    # ------------------------------------------------------------------
    def _dividir_en_chunks(self, texto: str, fuente: str, chunk_size: int = 500) -> List[str]:
        palabras = texto.split()
        chunks = []
        
        for i in range(0, len(palabras), chunk_size):
            chunk = ' '.join(palabras[i:i + chunk_size])
            chunk_con_meta = f"[Fuente: {os.path.basename(fuente)}]\n{chunk}"
            chunks.append(chunk_con_meta)
        
        return chunks
    
    def _limpiar_contexto(self, contexto: str) -> str:
        lineas = contexto.split('\n')
        lineas_unicas = []
        lineas_vistas = set()
        
        for linea in lineas:
            linea_limpia = linea.strip()
            if linea_limpia and linea_limpia not in lineas_vistas:
                lineas_vistas.add(linea_limpia)
                lineas_unicas.append(linea_limpia)
        
        return '\n'.join(lineas_unicas)
    
    def obtener_estadisticas(self) -> Dict:
        return {
            "total_chunks": self.collection.count(),
            "archivos_procesados": len(self.processed_files),
            "directorio_persistencia": self.persist_directory,
            "ruta_documentos": self.documentos_path
        }


# ------------------------------------------------------------------
# Prueba automática al ejecutar directamente
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("🧪 Probando RAGBuscador...")
    rag = RAGBuscador()
    
    # Prueba de búsqueda
    pregunta = "¿Cuáles son los requisitos de titulación?"
    contexto = rag.buscar_contexto(pregunta)
    
    if contexto:
        print("🔍 Contexto encontrado:")
        print(contexto[:500] + "...")
    else:
        print("❌ No se encontró contexto relevante")
    
    stats = rag.obtener_estadisticas()
    print(f"\n📊 Estadísticas: {stats}")