**Nombre del Repositorio:** Beautiful_Soup_Scraper

**Descripción:**
Este repositorio contiene un script de Python que utiliza la biblioteca `BeautifulSoup` para extraer y descargar contenido de capítulos de https://tunovelaligera.com, un sitio donde hay novelas que se pueden leer en linea pero no descargar. El script está diseñado para navegar por la estructura de la novela en cuestio de forma progresiva, identificando  capítulos y descargargandolos como archivos de texto (.txt).


**Características:**
* **Scraper Web Dirigido**: El script está diseñado para extraer contenido de capítulos de un sitio web específico, asegurándose de que solo se recopile datos relevantes.
  
* **Identificación Eficiente de Capítulos**: El script utiliza `BeautifulSoup` `re` `request` para analizar la estructura HTML del sitio web y identificar los capítulos, permitiendo una extracción de datos precisa y eficiente.
  
* **Salida de Archivos de Texto**: El contenido de los capítulos extraído se guarda como archivos de texto, lo que facilita la lectura, análisis o procesamiento adicional.
  

**Cómo Funciona:**
1. El script envía una solicitud HTTP al sitio web objetivo y recopila el contenido HTML.
2. `BeautifulSoup` se utiliza para analizar el HTML y identificar el enlace al capitulo siguiente.
3. El script navega a cada enlace de capítulo, extrae el contenido del capítulo y lo guarda como un archivo de texto.

**Requisitos:**
* Python 3.x
* Biblioteca `BeautifulSoup`
* Biblioteca `requests`
* Biblioteca `re`

**Uso:**
1. Clona este repositorio en tu máquina local.
2. Instala las bibliotecas requeridas ejecutando `pip install -r requirements.txt` (Aun no configurado, proximamente...).
3. Configura el script modificando las variables `base_url` para apuntar al sitio web y capítulos deseados.
4. Ejecuta el script utilizando `python web_scraper.py`.

**Nota:**
* Este script está destinado para uso personal y educativo solo. Asegúrate de revisar los términos de uso y el archivo robots.txt del sitio web para asegurarte de que el scraping de la web esté permitido.
* El script puede requerir modificaciones para adaptarse a cambios en la estructura o contenido del sitio web.
Al utilizar este script, podrás descargar y acceder fácilmente al contenido de los capítulos de tus libros favoritos, mientras aprendes sobre scraping de la web y programación en Python. ¡Disfruta codificando!
