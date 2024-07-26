import pandas as pd
import os
import html

#region CONSTANTES
# Ruta del archivo
ARCHIVO_XLS = '/DescripcionesExtract/eppendorf_clean.xlsx'
# Ruta de la carpeta de destino
RUTA_DESTINO = '/descripciones_ampliadas/'
# Ruta de mi proyecto
RUTA_BASE = 'C:/Users/Mario/Documents/Proquinorte' # os.getcwd().replace('\\','/')
# Columnas del archivo
TITULO_SKU = 'SKU'
TITULO_DESCRIPCION = 'Descripción Ampliada'
#endregion

def CrearCarpeta(carpeta_destino):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

def ConvertirAHTML(contenido: str):
    if '/>' not in contenido or '</' not in contenido:
        contenido = contenido.replace('\n','<br/>')
        contenido = contenido.replace('\t','&ensp;')
        resultado = contenido.encode("ascii", "xmlcharrefreplace").decode('utf_8') #html.escape(contenido)
    else:
        resultado = contenido
    return resultado

def RecorrerArchivo():
    # Leer el archivo Excel
    archivo = f'{RUTA_BASE}/{ARCHIVO_XLS}'
    print(f'Leyendo archivo {archivo}...')
    df = pd.read_excel(archivo, dtype={TITULO_SKU: str, TITULO_DESCRIPCION: str}, header=0)
    CrearCarpeta(RUTA_BASE+RUTA_DESTINO)
    for index, row in df.iterrows():
        # Buscar en la ruta de origen el nombre de la categoria origen. 
        sku = str(row[TITULO_SKU])
        descripcion_ampliada = str(row[TITULO_DESCRIPCION])        
        nombre_archivo = f'{RUTA_BASE}{RUTA_DESTINO}{sku}.txt'
        if len(descripcion_ampliada)>10:
            html_content = ConvertirAHTML(descripcion_ampliada)
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(html_content)
                print(f'Archivo creado: {nombre_archivo}')


RecorrerArchivo()