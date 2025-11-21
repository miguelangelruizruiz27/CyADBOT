# ---------------------------------------------------------------
# Módulo: base_datos.py (VERSIÓN FINAL)
# Autor: Miguel Ruiz
# Proyecto: CyADBot - UAM Azcapotzalco
# ---------------------------------------------------------------

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import unicodedata
import os
from dotenv import load_dotenv
from rapidfuzz import process, fuzz

# Cargar .env
load_dotenv()


class BaseDeDatos:

    def __init__(self):
        self.config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }

        self._verificar_conexion()

    # ---------------------------------------
    # 🔌 Conexión
    # ---------------------------------------
    def obtener_conexion(self):
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            print(f"❌ Error conectando a MySQL: {e}")
            return None

    def _verificar_conexion(self):
        try:
            conn = self.obtener_conexion()
            if conn and conn.is_connected():
                print("✅ Conexión MySQL OK")
                conn.close()
        except:
            print("❌ No se pudo conectar a MySQL")

 # ===========================================================
# 🔍 BUSCAR EN FAQS (versión final)
# ===========================================================
    def buscar_preguntas_frecuentes(self, consulta, categoria_principal=None):

        conn = self.obtener_conexion()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)

            # Filtrar por categoría si se proporciona
            if categoria_principal:
                cursor.execute("""
                    SELECT categoria_principal, subcategoria, pregunta, respuesta
                    FROM faqs
                    WHERE categoria_principal = %s
                """, (categoria_principal,))
            else:
                cursor.execute("""
                    SELECT categoria_principal, subcategoria, pregunta, respuesta
                    FROM faqs
                """)

            faqs = cursor.fetchall()
            if not faqs:
                return None

            # Normalizar textos
            def normalizar(s):
                s = "".join(
                    c for c in unicodedata.normalize("NFD", s.lower())
                    if unicodedata.category(c) != "Mn"
                )
                return s.replace("¿","").replace("?","").replace("¡","").replace("!","")

            consulta_norm = normalizar(consulta)
            preguntas_norm = [normalizar(f["pregunta"]) for f in faqs]

            # Rapidfuzz → devuelve (match, score, index)
            resultado = process.extractOne(
                consulta_norm,
                preguntas_norm,
                scorer=fuzz.token_set_ratio
            )

            if not resultado:
                return None

            mejor, score, idx = resultado

            # UMBRAL ALTO
            if score < 70:
                return None

            # Coincidencia de tokens
            tokens_p = set(consulta_norm.split())
            tokens_f = set(preguntas_norm[idx].split())
            if len(tokens_p & tokens_f) == 0:
                return None

            return faqs[idx]["respuesta"]

        except Exception as e:
            print(f"❌ Error buscando FAQs: {e}")
            return None

        finally:
            conn.close()


    # ===========================================================
    # 📝 REGISTRAR CONSULTAS NO RESUELTAS
    # ===========================================================
    def registrar_consulta_no_resuelta(self, texto_consulta):

        conn = self.obtener_conexion()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO consultas_sin_respuesta (pregunta, fecha) VALUES (%s, %s)",
                (texto_consulta, datetime.now())
            )
            conn.commit()
            print(f"📝 Consulta no resuelta registrada: {texto_consulta}")

        except Exception as e:
            print(f"❌ Error registrando consulta no resuelta: {e}")

        finally:
            conn.close()
