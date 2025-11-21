# ---------------------------------------------------------------
# Módulo: filtro_contenido.py
# Descripción: Filtra mensajes no académicos y sanitiza la entrada
#              del usuario para prevenir inyección de código.
# Autor: Miguel Ruiz
# Proyecto: CyADBot - UAM Azcapotzalco
# ---------------------------------------------------------------

# Importar la función escape de markupsafe para limpiar texto HTML
from markupsafe import escape
# Importar el módulo re para usar expresiones regulares
import re


class FiltroContenido:
    """Clase encargada de filtrar contenido irrelevante y sanitizar texto."""

    def __init__(self):
        # Lista de patrones que identifican temas no académicos
        # Cada elemento es una expresión regular (regex)
        self.patrones_no_academicos = [
            r'.*futbol.*',      
            r'.*deporte.*',     
            r'.*pelicula.*',     
            r'.*netflix.*',      
            r'.*musica.*',       
            r'.*cancion.*',      
            r'.*videojuego.*',   
            r'.*juego.*',        
            r'.*comida.*',       
            r'.*restaurante.*',  
            r'.*receta.*',       
            r'.*tienda.*',       
            r'.*clima.*',        
            r'.*temperatura.*',  
            r'.*chiste.*',      
            r'.*broma.*'         
        ]
    
    def es_relevante(self, texto):
        """
        Evalúa si el texto ingresado por el usuario es relevante
        para temas académicos. Si coincide con algún patrón no académico,
        retorna False; de lo contrario, True.
        """
        # Convertir todo el texto a minúsculas para evitar errores de comparación
        texto_lower = texto.lower()
        
        # Revisar cada patrón definido en la lista
        for patron in self.patrones_no_academicos:
            # Si el texto coincide con un patrón no académico
            if re.match(patron, texto_lower):
                # Mostrar mensaje en consola indicando que se filtró el contenido
                print(f"❌ Contenido filtrado: '{texto}'")
                # Indicar que el texto no es relevante
                return False
        
        # Si ningún patrón coincide, el texto se considera válido
        return True
    

    def sanitizar(self, texto):
        """
        Limpia el texto de entrada reemplazando caracteres especiales
        por sus equivalentes seguros en HTML.
        Esto previene ataques de tipo Cross-Site Scripting (XSS).
        """
        # Aplicar escape() para neutralizar etiquetas HTML o scripts
        sanitized = escape(texto)
        print("🧼 Sanitizado:", sanitized)
        # Convertir el resultado (objeto Markup) a una cadena normal
        return str(sanitized)
    

