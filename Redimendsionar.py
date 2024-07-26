import cv2
import os

# Directorio de origen y destino
input_dir = r"C:\Users\Usuario\Desktop\sacar\carloerba"
#80x64
#output_dir = r"C:\Users\Usuario\Desktop\sacar\fotosskuAgilent\80x64"
#new_size = (80, 64)
#120x100
#output_dir = r"C:\Users\Usuario\Desktop\sacar\fotosskuAgilent\120x100"
#new_size = (120,100)
#137x72
output_dir = r"C:\Users\Usuario\Desktop\sacar\fotosskuAgilent\120x100"
new_size = (120,100)
os.makedirs(output_dir, exist_ok=True)

# Tamaño al que se redimensionarán las imágenes
# Recorrer todos los archivos en el directorio de entrada
for filename in os.listdir(input_dir):
    # Construir la ruta completa del archivo
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)
    
    # Leer la imagen
    img = cv2.imread(input_path)
    if img is not None:
        # Redimensionar la imagen
        img_resized = cv2.resize(img, new_size)
        # Guardar la imagen redimensionada en el directorio de salida
        cv2.imwrite(output_path, img_resized)
    else:
        print(f"Error al leer la imagen {input_path}")

print("Redimensionado completado.")
