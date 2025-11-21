# ---------------------------------------------------------------
# Módulo: clasificador_intencion.py
# Autor: Miguel Ruiz
# Proyecto: CyADBot - UAM Azcapotzalco
# ---------------------------------------------------------------

import spacy

class ClasificadorIntencion:

    def __init__(self):
        try:
            self.nlp = spacy.load("es_core_news_md")
            print("✅ spaCy MD cargado")
        except:
            self.nlp = spacy.load("es_core_news_sm")
            print("⚠️ spaCy SM cargado (menor precisión)")

        # CATEGORÍAS PRINCIPALES → para FAQs
        self.desc_categoria = {
            "DUDAS GENERALES": (
                "profesores profesoras maestros maestras donde encuentro ubicacion "
                "localizar ubicar salon oficina encontrar docente docentes contacto "
                "correos informacion general cead edificios aulas ubicacion"
            ),

            "TRÁMITES ESCOLARES": (
                "inscripcion reinscripcion ueas cambio turno constancias revalidacion "
                "tramites documentos escolares secretaria proceso administrativo"
            ),

            "SITUACIONES IRREGULARES Y DE RIESGO": (
                "reprobar reprobé calificación inasistencias baja abandono quinta oportunidad "
                "recuperacion rectificacion revision promedio situacion irregular riesgo academico"
            ),

            "OTROS TEMAS": (
                "otros temas varias dudas diversas preguntas adicionales ayuda especial"
            )
        }

        # DOCUMENTOS TXT → para búsqueda semántica
        self.desc_documentos = {
            "Reglamento alumnado.txt": (
                "reglamento alumnado alumnos normativa reglas articulos sanciones obligaciones derechos disciplina "
                "consecuencias disposiciones oficiales faltas normas juridico"
            ),

            "Guia Nuevo Ingreso.txt": (
                "guia nuevo ingreso pivu becas servicios deportes talleres horarios tutorias "
                "ubicar maestros profesores vida universitaria oficinas aulas cead mapa"
            )
        }

    def clasificar_categoria(self, texto):
        doc = self.nlp(texto.lower())
        mejor = "OTROS TEMAS"
        score_max = 0

        for cat, desc in self.desc_categoria.items():
            score = doc.similarity(self.nlp(desc))
            if score > score_max:
                mejor = cat
                score_max = score

        if score_max < 0.50:
            return "OTROS TEMAS"

        return mejor

    def clasificar_documento(self, texto):
        doc = self.nlp(texto.lower())
        puntajes = {}

        for nombre, desc in self.desc_documentos.items():
            puntajes[nombre] = doc.similarity(self.nlp(desc))

        ordenados = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
        mejor_doc, score = ordenados[0]

        if score < 0.28:
            return list(self.desc_documentos.keys())

        return [mejor_doc]

    def clasificar(self, texto):
        return self.clasificar_categoria(texto), self.clasificar_documento(texto)
