from PIL import Image
import pandas as pd
import os
import requests

#region CONSTANTES
# Ruta del archivo
ARCHIVO_EXCEL = 'carloerba.xlsx'
# Ruta de la carpeta de origen
IMAGENES_ORIGEN = '/ImagenOrigen/'
# Ruta de la carpeta de destino
IMAGENES_DESTINO = '/fotossku/'
# Lista de extensiones posibles
EXTENSIONES_IMAGENES = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff']
EXTENSION_IMAGEN_OPTIMIZADA = 'PNG'
# Ruta de mi proyecto
RUTA_BASE = os.getcwd().replace('\\','/')
# Columnas del archivo
TITULO_SKU = 'SKU'
TITULO_IMAGEN = 'Enlace_de_imagen'
# URL de Imagen no encontrada
IMAGEN_NO_ENCONTRADA = 'https://proquiwebep.azureedge.net/cdnfiles/nc/Productos/notfound.jpg'
RUTA_CDN = 'https://proquiwebep.azureedge.net/cdnfiles/nc/Productos/'
#endregion


def eliminar_punto_final(texto):
    if texto.endswith('.'):
        return texto[:-1]
    else:
        return texto

def encontrar_archivo_con_extension(nombre_archivo, carpeta_origen, extensiones):
    for ext in extensiones:
        archivo = os.path.join(carpeta_origen, nombre_archivo + ext)
        if os.path.isfile(archivo):
            return archivo
    return None

def optimize_and_resize_image(archivo_origen, archivo_destino, size=(600, 600), quality=85):
    with Image.open(archivo_origen) as img:
        img = img.convert("RGB")  # Asegurarse de que esté en modo RGB
        img = img.resize(size, Image.ANTIALIAS)
        img.save(archivo_destino, EXTENSION_IMAGEN_OPTIMIZADA, optimize=True, quality=quality)

def CrearCarpeta(carpeta_destino, size=(600, 600)):
    carpeta_destino_size = carpeta_destino + "_" + "x".join(map(str, size))
    if not os.path.exists(carpeta_destino_size):
        os.makedirs(carpeta_destino_size)
        return True
    else:
        return False

def process_image(archivo_origen, nombre_archivo,carpeta_destino, size=(600, 600), quality=85):
    if(CrearCarpeta(carpeta_destino,size)):    
        nombre_archivo = os.path.join(carpeta_destino, nombre_archivo + f".{EXTENSION_IMAGEN_OPTIMIZADA.lower()}")
        if nombre_archivo.lower().endswith(EXTENSIONES_IMAGENES):        
            output_path = os.path.join(carpeta_destino, nombre_archivo)
            optimize_and_resize_image(archivo_origen, output_path, size, quality)
            return output_path
    return None


def list_files(path):
    all_entries = os.listdir(path)
    i=1
    for entry in all_entries:
        if os.path.isfile(os.path.join(path, entry)):
            print(f"File #{i}:{entry}")
            i=i+1

def RecorrerArchivo():
    # Leer el archivo Excel
    df = pd.read_excel(ARCHIVO_EXCEL, dtype={TITULO_SKU: str}, header=0)    
    for index, row in df.iterrows():
        # Nombre del archivo en la columna A
        nombre_archivo = eliminar_punto_final(str(row['Nombre']))
        # Nuevo nombre del archivo en la columna B
        nuevo_nombre_archivo = str(row['SKU'])        
        # Enlace de imagen
        enlace_de_imagen = str(row['Enlace_de_imagen'])
        # Ruta completa del archivo de origen
        archivo_origen = encontrar_archivo_con_extension(nombre_archivo, imagenes_origen, EXTENSIONES_IMAGENES)        
        # Verificar si el archivo existe
        process_image(archivo_origen,nuevo_nombre_archivo,IMAGENES_DESTINO)

def ObtenerImagen(imagen_url):    
    response = requests.get(imagen_url)
    if response.status_code == 200 and response.content != b'':
        return response
    else:
        return None

def GuardarImagen(imagen,sku,imagenes_destino):
    ruta_destino = f'{imagenes_destino}/{sku}.png'
    if(imagen==None):
        ruta_imagen = IMAGEN_NO_ENCONTRADA
    else:
        ruta_imagen = ruta_destino
        with open(ruta_destino,'wb') as file:
            for chunk in imagen.iter_content(1024):
                # Write each chunk to the file
                file.write(chunk)
    return {
        'sku':sku,
        'ruta_imagen': ruta_imagen
    }

def VerificarRuta(ruta_destino):
    directorio = os.path.dirname(ruta_destino)
    if not os.path.exists(directorio):
        os.makedirs(directorio)

def DescargarImagenes():
    # Leer el archivo Excel
    image_list = []
    df = pd.read_excel(ARCHIVO_EXCEL, dtype={TITULO_SKU: str}, header=0)
    filas_totales = df.shape[0]
    i=1
    VerificarRuta(imagenes_destino)
    for index, row in df.iterrows():
        print(f"Procesando imagen #{i} de {filas_totales}")
        sku = str(row[TITULO_SKU])
        imagen_url = str(row[TITULO_IMAGEN])
        
        if  "Productos/notfound.jpg" not in imagen_url:
            print(imagen_url)
            imagen = ObtenerImagen(imagen_url)
            dato_imagen=GuardarImagen(imagen,sku,imagenes_destino)
            image_list.append({
                'sku': dato_imagen.get('sku',''),
                'ruta_imagen': dato_imagen.get('ruta_imagen',''),
                'ruta_cdn': f"{RUTA_CDN}{os.path.basename(dato_imagen.get('ruta_imagen',''))}"
            })
        i=i+1
    return image_list

def CrearArchivosOptimizados(ruta_origen,imagenes,size=(600, 600), quality=85):
    optimizados = []
    carpeta_destino = "/" + "x".join(map(str, size))
    ruta_destino = ruta_origen + carpeta_destino
    for imagen in imagenes:
        sku = imagen.get('sku','')
        ruta_imagen = imagen.get('ruta_imagen','')





#===================================================================================
imagenes_origen = RUTA_BASE+IMAGENES_ORIGEN
imagenes_destino = RUTA_BASE+IMAGENES_DESTINO
imagenes = DescargarImagenes()
CrearArchivosOptimizados(ruta_origen,imagenes,size=(600, 600), quality=85)
#RecorrerArchivo()