Estructura del scraper...

1) Importacion librerias.

2) Variables globales:
    - Header
    - Url a scrapear.
    - Captura el endpoint de la serie

2) Funciones:
    - Obtener nombre de la serie.
    - Obtener numero de capitulo y volumen
    - Crear un archivo y lo retorna.
    - Obtiene el contenido del capitulo (Texto del capitulo)

3) Bucle
    - Obtiene la pagina (GET).                      Se debería llamar funcion()
    - Obtiene el numero de capitulo.                Se llama funcion()
    - Obtiene el volumen actual.                    Se llama funcion()
    - Chequea que no haya capítulos faltantes. 
    - Chequea que el código de respuesta es 200.
    - Obtiene texto de capitulo
    - Obtiene devuelta num capitulo !!!!!!!!!
    - Elimina determinado texto
    - Escribe el capitulo en el archivo
    - Lleva un contador, si se guardo determinada cantidad de capítulos crea un nuevo archivo.
    - Se obtiene el enlace al siguiente capitulo



Código ineficiente, repetido, mal organizado, engorroso, una vergüenza que esto este en mi portafolio. Refactorizar URGENTE...

