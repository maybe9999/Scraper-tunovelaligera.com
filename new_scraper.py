import requests, re
from bs4 import BeautifulSoup


#Global variables
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
initialUrl = input("Ingrese la URL del capitulo a obtener: ") or 'https://tunovelaligera.com/mi-sistema-de-fusion/mi-sistema-de-fusion-capitulo-1/'
archivo_actual = 0
capitulos_guardados = 0
arch_txt = None

#--------------------------------------------------------------------------------------------------------------#

#Functions
def fetch_page_content(url, head=header, retries=5, timeout=5):
    for attempt in range(retries):
        try:
            page = requests.get(url, headers=head, timeout=timeout)
            if page.status_code == 200:
                print("Fetch: 200 OK")
                soup = BeautifulSoup(page.text, 'html.parser')
                return [page, soup]
            else:
                print(f'No se pudo obtener la página {url}.')
        except requests.exceptions.Timeout as err:
            print("\n\n\n---------TimeOut---------\n\n\n",err,"\n"*4,"Reintentando")
        except Exception as err:
            print("\n\n\n---------Error!!!---------\n\n\n",err,"\n"*4,"Reintentando...")
    return "Error al obtener el contenido de la pagina"

def get_chapter_content(soup_function): #Se puede y se debe mejorar (arreglar)
    elements = soup_function.find_all(class_= lambda x : x and x.startswith("entry-content"))
    devolucion = []
    # Itera a través de los elementos encontrados
    for element in elements:
        # Obtiene todas las clases del elemento como una lista
        classes = element["class"]
        # Itera a través de las clases
        for class_name in classes:
            # Verifica si la clase comienza con "entry-content"
            if class_name.startswith("entry-content"):
                devolucion.append(re.findall(r'\d+', str(class_name)))
            else:
                try:
                    int(class_name)
                    devolucion.append(class_name)
                except:
                    pass
    try:
        historia_element = soup_function.find('div', class_=f"entry-content_wrap_s_{devolucion[0][0]}")
    except:
        try:
            historia_element = soup_function.find('div', class_=f"entry-content_wrap_s_{devolucion[0][1]}")
        except:
            try:
                historia_element = soup_function.find('div', class_=f"entry-content_wrap_s_{devolucion[0]}")
            except:
                historia_element = soup_function.find('div', class_=f"entry-content_wrap_s_{devolucion}")
    
    historia_element = historia_element.get_text()
    historia_final = re.sub(r'\n+', '\n', historia_element) #Remplaza saltos de linea consecutivos por solo 1 salto
    historia_final2 = re.search(r"(.*?)Guardar Capitulo", historia_final, re.DOTALL).group(1).strip()
    return historia_final2

def create_new_file(seriesName="Unknown", currentVolume="X", currentChapter=0):
    global archivo_actual, arch_txt
    archivo_actual += 1
    arch_txt = open(f'-{seriesName}...V_{currentVolume}...C_{currentChapter}.txt', 'a', encoding='utf-8')

def get_series_name(url):
    return re.search(r'tunovelaligera\.com/([^/]+)/', url).group(1) or "Unknown"

def get_current_volume(url):
    try:
        return re.search(r'volumen.*?(\d+)',url).group(1)
    except AttributeError as err:
        print("Numero de volumen no encontrado...")
        return "X"
    
def get_number_of_chapter(url):
    return re.search(r'capitulo.*?(\d+)', url).group(1) or re.search(r'(\d+)', url).group(1)

def get_link_next_chapter(soup_function):
    try:
        return soup_function.find('a', href=True, text="Siguiente Capítulo")['href']
    except Exception as err:
        print("Error al obtener el link del siguiente capitulo. Razon: ", "Capitulo final" if isinstance(err, TypeError) else f"Desconocida... Error:{err}")
        return None

def msj_console():
    print(f"Volumen: {current_volume}, Chapter: {current_chapter}")
    print(f"Archivo actual {archivo_actual}\n")
    print(f"Link actual: {initialUrl}")
    print("Next Chapter...")

#--------------------------------------------------------------------------------------------------------------#

while True:
    current_volume = get_current_volume(initialUrl)
    current_chapter = get_number_of_chapter(initialUrl)

    #Crea archivos con hasta 100 capitulos cada uno
    if capitulos_guardados >= 100 or capitulos_guardados == 0:
        if capitulos_guardados >= 100:
            arch_txt.close()
        name_series = get_series_name(initialUrl)
        create_new_file(seriesName=name_series, currentVolume=current_volume, currentChapter=current_chapter)
        arch_txt.write("ï»¿" + "\n")
        capitulos_guardados = 0
        
    page, soup = fetch_page_content(initialUrl)
    chapter_content = get_chapter_content(soup)

    arch_txt.write("-"*100 +f"\n {name_series}\nVolumen: {current_volume}, Capitulo:{current_chapter} \n{chapter_content}"+"\n"*12)
    capitulos_guardados += 1
    msj_console()

    initialUrl = get_link_next_chapter(soup)

    if not initialUrl:
        print("Finalizando programa")
        break