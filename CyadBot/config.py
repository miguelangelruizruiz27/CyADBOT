# ---------------------------------------------------------------
# Módulo: config.py
# Descripción: Define la configuración base del sistema CyADBot,
#              incluyendo parámetros de conexión, rutas y seguridad.
# Autor: Miguel Ruiz
# Proyecto: CyADBot - UAM Azcapotzalco
# ---------------------------------------------------------------

# Importar módulo 'os' para manejar rutas y operaciones del sistema
import os


class Config:
    """
    Clase de configuración global del sistema.
    Contiene las variables y parámetros base que utiliza CyADBot
    para conectarse a la base de datos, definir rutas internas y
    establecer configuraciones de seguridad.
    """

    # -----------------------------------------------------------
    # Sección: Configuración de la base de datos MySQL
    # -----------------------------------------------------------

    # Dirección del servidor de base de datos (localhost = máquina local)
    MYSQL_HOST = 'localhost'

    # Usuario con permisos de acceso a la base de datos
    MYSQL_USER = 'root'

    # Contraseña del usuario definido
    MYSQL_PASSWORD = 'root'

    # Nombre de la base de datos donde se almacenan las tablas de CyADBot
    MYSQL_DATABASE = 'cyadbot_db'


    # -----------------------------------------------------------
    # Sección: Configuración del framework Flask
    # -----------------------------------------------------------

    # Clave secreta utilizada por Flask para manejar sesiones,
    # autenticación y protección frente a ataques CSRF.
    SECRET_KEY = '1234'


    # -----------------------------------------------------------
    # Sección: Definición de rutas internas del proyecto
    # -----------------------------------------------------------

    # Obtiene la ruta absoluta del directorio donde se encuentra este archivo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Ruta donde se almacenarán los documentos institucionales
    # dentro del directorio 'static/documents'
    DOCUMENTS_DIR = os.path.join(BASE_DIR, 'static', 'documents')

    # Ruta al directorio de datos o recursos adicionales (JSON, etc.)
    DATA_DIR = os.path.join(BASE_DIR, 'data')


    # -----------------------------------------------------------
    # Sección: Verificación de rutas al iniciar la aplicación
    # -----------------------------------------------------------

    # Si el directorio de documentos no existe, se crea automáticamente.
    if not os.path.exists(DOCUMENTS_DIR):
        os.makedirs(DOCUMENTS_DIR)
        # Mensaje informativo en consola al crear la carpeta
        print(f"📁 Carpeta 'documents' creada: {DOCUMENTS_DIR}")


# ---------------------------------------------------------------
# Bloque de prueba rápida (solo se ejecuta si se corre directamente)
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Indica en consola que la configuración se cargó correctamente
    print("🔧 Configuración cargada correctamente")

    # Muestra la ruta absoluta de la carpeta de documentos
    print(f"📁 Documents dir: {Config.DOCUMENTS_DIR}")

    # Muestra el nombre de la base de datos configurada
    print(f"📊 MySQL database: {Config.MYSQL_DATABASE}")
