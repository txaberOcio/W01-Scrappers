from PIL import Image
import pandas as pd
import csv
import os

#region CONSTANTES
# Ruta del archivo
ARCHIVO_CSV = 'RenovacionCategoria.csv'
# Ruta de la carpeta de origen
IMAGENES_ORIGEN = '/category-images/'
# Ruta de la carpeta de destino
IMAGENES_DESTINO = '/new-category-images/'
# Lista de extensiones posibles
EXTENSIONES_IMAGENES = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff']
EXTENSION_IMAGEN_OPTIMIZADA = 'PNG'
# Ruta de mi proyecto
RUTA_BASE = 'C:/Users/Mario/Documents/Proquinorte' # os.getcwd().replace('\\','/')
# Columnas del archivo
TITULO_ANTERIOR = 'Categoría Antigua'
TITULO_NUEVA = 'Categoría Nueva'
#endregion


def encontrar_archivo_con_extension(nombre_archivo, carpeta_origen, extensiones):
    for ext in extensiones:
        archivo = os.path.join(carpeta_origen, nombre_archivo + ext)
        if os.path.isfile(archivo):
            return archivo
    return None


def CrearCarpeta(carpeta_destino):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

def ImprimirCSV(no_encontrados):
    print('Imprimiendo...')
    csv_file_name = f'{RUTA_BASE}/no_encontrados.csv'
    with open(csv_file_name, 'w', newline='',encoding='utf-8') as csvfile:
        fieldnames = ['Categoría Antigua', 'destino_faltante', 'Categoría Nueva']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in no_encontrados:
            writer.writerow(data)         

def RecorrerArchivo(no_encontrados):
    # Leer el archivo Excel
    archivo = f'{RUTA_BASE}/{ARCHIVO_CSV}'
    df = pd.read_csv(archivo, dtype={TITULO_ANTERIOR: str, TITULO_NUEVA: str}, header=0)
    CrearCarpeta(RUTA_BASE+IMAGENES_ORIGEN)
    for index, row in df.iterrows():
        # Buscar en la ruta de origen el nombre de la categoria origen. 
        categoria_anterior = str(row[TITULO_ANTERIOR])
        categoria_nueva = str(row[TITULO_NUEVA])
        archivo_origen = encontrar_archivo_con_extension(categoria_anterior,RUTA_BASE+IMAGENES_ORIGEN, EXTENSIONES_IMAGENES)
        if archivo_origen == None:
            no_encontrados.append({
                TITULO_ANTERIOR: categoria_anterior,
                TITULO_NUEVA: categoria_nueva,
                'destino_faltante': f'{RUTA_BASE+IMAGENES_DESTINO+categoria_nueva}.png'
            })
            print(f'Archivo no encontrado:{RUTA_BASE+IMAGENES_ORIGEN+categoria_anterior}.*')
        else:
            # Cargar el archivo
            image = Image.open(archivo_origen)
            if image.mode == 'CMYK':
                image = image.convert('RGB')
            # Guardar el archivo con el nuevo nombre. 
            archivo_destino = f'{RUTA_BASE+IMAGENES_DESTINO+categoria_nueva}.png'
            image.save(archivo_destino, format='PNG')

no_encontrados = []
RecorrerArchivo(no_encontrados)
ImprimirCSV(no_encontrados)
        
        








