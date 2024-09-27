import requests, re
from time import sleep
from bs4 import BeautifulSoup

hea = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
# Definir la URL inicial

base_url ='https://tunovelaligera.com/mi-sistema-de-fusion/mi-sistema-de-fusion-capitulo-1/'


print(base_url)

resultado = re.search(r'\/([a-zA-Z0-9-]+)\/([a-zA-Z0-9-]+)-capitulo-(\d+)\/', base_url)
def name_s(result):
    try:
        name_serie = result.group(1)
    except:
        name_serie = re.search(r'tunovelaligera\.com/([^/]+)/',base_url).group(1)
        return name_serie
def num_s(result=""):
    try:
        num_capitulo = result.group(3)
    except:
        try:
            num_capitulo = re.search(r'capitulo-(\d+)',base_url).group(1)
        except:
            num_capitulo = re.search(r'-(\d+)',base_url).group(1)
    return num_capitulo

nombre_serie, numero_capitulo = name_s(resultado), num_s(resultado)

capitulo_anterior= int(numero_capitulo)
pa_no_se = ""
volumen=""
 
# Inicializar el contador de capítulos y archivo actual
capitulos_guardados = 1
archivo_actual = 1
def busca_en():
    # Encuentra todos los elementos que tienen una clase que comienza con "entry-content"
    elements = soup.find_all(class_=lambda x: x and x.startswith("entry-content"))
    devolucion = []
    # Itera a través de los elementos encontrados
    for element in elements:
        # Obtiene todas las clases del elemento como una lista
        classes = element["class"]
        # Itera a través de las clases
        for class_name in classes:
            #print(class_name,"\n.......")
            # Verifica si la clase comienza con "entry-content"
            if class_name.startswith("entry-content"):
                devolucion.append(re.findall(r'\d+', str(class_name)))
            else:
                try:
                    int(class_name)
                    devolucion.append(class_name)
                except:
                    pass
    #print(len(devolucion),"\n",devolucion,"\n",type(devolucion))
    return devolucion
    
def arch():
    global arch_text, nombre_serie, archivo_actual, numero_capitulo
    numero_cap_txt = numero_capitulo
    arch_txt = open(f'-{nombre_serie}_{numero_capitulo}.txt', 'a', encoding='utf-8')
    return arch_txt
arch_txt= arch()

while base_url and archivo_actual <= 10000:  # Cambia el 2 por el número deseado de archivos
    try:
        page = requests.get(base_url, headers=hea, timeout=5)
    except requests.exceptions.Timeout as err:
        print("\n\n\nTimeOut\n\n\n",err,"\n"*4,"Reintentando")
        page = requests.get(base_url, headers=hea, timeout=5)

    numero_capitulo = num_s()
    
    print("Capitulo: ",numero_capitulo)
    
    try:
        volumen = re.search(r'volumen-(\d+)',base_url).group(1)
        print(volumen)
        if int(volumen)>=1:
            print("volumen ok")
            volumen =f'Volumen: {volumen}'
        else:
            print("volumen bad")
            volumen=""
    except:
        pass
    if int(capitulo_anterior) +1 != int(numero_capitulo) and capitulos_guardados!=0:
        pa_no_se = f"Faltan los capitulos {list(range(int(capitulo_anterior)+1,int(numero_capitulo),1))}"
        capitulo_anterior = int(numero_capitulo)
    else:
        capitulo_anterior = int(numero_capitulo)
        pa_no_se = ""
        
    if page.status_code != 200:
        print(f'No se pudo obtener la página {base_url}. Saliendo...')
        page = requests.get(base_url, headers=hea)
    else:
        print("Page status ok")
    soup = BeautifulSoup(page.text, 'html.parser')
    
    entrada = busca_en()
    
    try:
        historia_element = soup.find('div', class_=f"entry-content_wrap_s_{entrada[0][0]}")
    except:
        historia_element = soup.find('div', class_=f"entry-content_wrap_s_{entrada[0][1]}")

    try:
        Cap_y_name = str(soup.find('div'))
        Cap_y_name = Cap_y_name[Cap_y_name.index("Capítulo"):Cap_y_name.index("Capítulo")+40]
        n_c = re.search(r'(Capítulo \d+.*?)<', Cap_y_name).group(0)
    except:
        n_c = f"\n Capitulo: {numero_capitulo} \n {pa_no_se}"
    
    if historia_element:
        historia = historia_element.get_text(separator="\n")
        historia = historia.replace('Leer en tunovelaligera.com', '')
        historia = historia.replace('Editado por: Dr.Lock','')
        historia = historia[:historia.find("Guardar Capitulo")]

        # Guardar la historia en un archivo de texto
        arch_txt.write("ï»¿"+"--------------"*8+f"\n \n \n \n \n {volumen} {n_c[:-1]} \n {historia}\n\n\n\n\n")

        print(" Saved...",capitulos_guardados,"\n \n \n \n")
        capitulos_guardados += 1

        # Si se han guardado 100 capítulos, cambiar al siguiente archivo
        if capitulos_guardados > 100:
            print("Nuevo archivo")
            archivo_actual += 100
            capitulos_guardados = 1
            arch_txt=arch()
    elif not historia_element:
        historia_element = soup.find('div', class_=f"entry-content_tnl_{entrada[0][0]}")
        if historia_element:
            historia = historia_element.get_text(separator="\n")
            historia = historia.replace('Leer en tunovelaligera.com', '')
            historia = historia.replace('Editado por: Dr.Lock','')
            historia = historia[:historia.find("Guardar Capitulo")]

            # Guardar la historia en un archivo de texto
            arch_txt.write("ï»¿"+"--------------"*8+f"\n\n {n_c[:-1]} \n\n {historia}\n\n\n\n\n")
   
            print(capitulos_guardados)
            capitulos_guardados += 1

            # Si se han guardado 100 capítulos, cambiar al siguiente archivo
            if capitulos_guardados > 100:
                arch_txt.close()
                archivo_actual += 100
                capitulos_guardados = 1
                arch_txt= arch()
        else:
            print(historia_element,"error 2 no se guardo")
    else:
        print(historia_element,"error no se guardo")
        
    # Encontrar el enlace a la página siguiente
    all_links = str(soup.find('div'))
    """
    open(f'sopa.txt','a').write(all_links)

    try:
        base_url = re.search(r'href="(.*?)"', all_links[all_links.index("Capitulo Siguiente"):]).group(1)
    except ValueError:
        print("No se encontraron mas capitulos")
        break
    print(base_url, "url ok")
"""

        # Expresión regular para extraer la sección de código que contiene el enlace
    section_pattern = r'<div class="nav-next nav-button">(.*?)Siguiente Capítulo</a>'
    
    # Buscar la sección de código en el texto HTML
    section_match = re.search(section_pattern, all_links, re.DOTALL)
    
    # Si se encuentra la sección de código, extraer el enlace
    if section_match:
        section_code = section_match.group(1)
        
        # Expresión regular para extraer el enlace dentro de la sección de código
        link_pattern = r'href="([^"]+)"'
        link_match = re.search(link_pattern, section_code)
        
        if link_match:
            next_chapter_link = link_match.group(1)
            print(f"Enlace al siguiente capítulo: {next_chapter_link}")
            base_url = next_chapter_link
            print(base_url)
            sleep(1)
        else:
            print("No se encontró el enlace en la sección de código.")
    else:
        print("No se encontró la sección de código que contiene el enlace al siguiente capítulo.")
print("Fin del proceso")
try:
    if err:
        print(err)
except:
    pass
