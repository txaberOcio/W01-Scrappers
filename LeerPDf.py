import pandas as pd
import PyPDF2
import re
import requests
from io import BytesIO

# Lee el archivo Excel (asegúrate de tener la biblioteca openpyxl instalada)
file_path = 'Productos con ficha seguridad.xlsx'
df = pd.read_excel(file_path)
mach = ""
# Función para descargar y extraer texto de un archivo PDF desde una URL
def extract_text_from_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        pdf_file = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el PDF: {e}")
        return None
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return None

# Busca las cadenas específicas en el texto
def check_for_strings(text):
    if text is None:
        return -1  # Error en la descarga o lectura del PDF
    keywords = ["R50", "R50/53", "R51/53", "H400", "H410", "H411"]
    for keyword in keywords:
        if re.search(keyword, text, re.IGNORECASE):
            mach=keyword
            return 1
    return 0

# Procesa cada URL en la columna D
for index, row in df.iterrows():
    pdf_url = row['D']
    product_name = row['A']  # Access product name from column A

    print(f"Procesando producto: {product_name} (URL: {pdf_url})")

    pdf_text = extract_text_from_pdf(pdf_url)
    df.loc[index, 'E'] = check_for_strings(pdf_text)

# Guarda el DataFrame actualizado en un nuevo archivo Excel
df.to_excel('archivo_actualizado.xlsx', index=False)
