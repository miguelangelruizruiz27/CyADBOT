# ---------------------------------------------------------------
# Módulo: procesador_preguntas.py (VERSIÓN SIN SPACY)
# ---------------------------------------------------------------

from filtro_contenido import FiltroContenido
from clasificador_intencion import ClasificadorIntencion
from base_datos import BaseDeDatos
from rag_busqueda import RAGBuscador


class ProcesadorPreguntas:

    def __init__(self):
        print("🔄 Inicializando ProcesadorPreguntas...")

        # Instancias internas (spacy está dentro de clasificador_intencion)
        self.filtro = FiltroContenido()
        self.clasificador = ClasificadorIntencion()
        self.base_datos = BaseDeDatos()

        # RAG local - AUTO-INICIALIZABLE
        print("🔄 Inicializando RAGBuscador...")
        self.rag = RAGBuscador(documentos_path="./static/documentos")
        print("✅ RAG listo")

        print("🚀 ProcesadorPreguntas inicializado correctamente")

    # ------------------------------------------------------------------
    # MÉTODO PRINCIPAL - CON DEBUG PARA TU PROBLEMA
    # ------------------------------------------------------------------
    def procesar_pregunta(self, pregunta):
        print(f"\n💬 Pregunta recibida: {pregunta}")

        # 1. Sanitizar
        pregunta_limpia = self.filtro.sanitizar(pregunta)
        print(f"🧼 Sanitizada: {pregunta_limpia}")
        
        if not self.filtro.es_relevante(pregunta_limpia):
            return "🤖 Solo puedo responder preguntas académicas relacionadas con CyAD."

        # 2. Clasificar
        categoria, documentos_sugeridos = self.clasificador.clasificar(pregunta_limpia)
        print(f"🎯 Intención: {categoria}")

        # 3. Buscar en FAQs - CON DEBUG DETALLADO
        print("🔎 Buscando en FAQs...")
        respuesta_faq = self.base_datos.buscar_preguntas_frecuentes(
            consulta=pregunta_limpia, categoria_principal=categoria
        )
        
        if respuesta_faq:
            print(f"✅ FAQ ENCONTRADA: {respuesta_faq[:100]}...")
            return respuesta_faq
        else:
            print("❌ NO se encontró en FAQs")

        # 4. Buscar en documentos
        print("🔍 Buscando en documentos RAG...")
        contexto = self.rag.buscar_contexto(pregunta_limpia)

        if contexto:
            print(f"✅ Contexto RAG encontrado: {contexto[:100]}...")
            return self.formatear_respuesta(contexto)
        else:
            print("❌ No se encontró en documentos RAG")

        # 5. Registrar no resuelta
        print("📝 Registrando como no resuelta...")
        self.base_datos.registrar_consulta_no_resuelta(pregunta_limpia)

        return "No se encontró información relacionada en los documentos."

    def formatear_respuesta(self, contexto):
        respuesta = contexto[:500].strip()
        if len(contexto) > 500:
            respuesta += "..."
        return f"📚 Según los documentos:\n\n{respuesta}"


# ------------------------------------------------------------------
# PRUEBA ESPECÍFICA para diagnosticar tu problema
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("🧪 PRUEBA ESPECÍFICA - Pregunta FAQ...")
    
    procesador = ProcesadorPreguntas()
    
    # Tu pregunta exacta que SÍ está en FAQs
    pregunta_test = "¿Cuál es el procedimiento para solicitar apoyo, emitir una queja o realizar un comentario o sugerencia?"
    
    print(f"\n❓ Pregunta FAQ: {pregunta_test}")
    respuesta = procesador.procesar_pregunta(pregunta_test)
    
    print(f"\n🤖 RESPUESTA FINAL: {respuesta}")