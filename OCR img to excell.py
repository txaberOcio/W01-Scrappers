import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import openpyxl
import pytesseract
from pytesseract import Output

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # Redimensionar la imagen para mostrar una vista previa
        img = ImageTk.PhotoImage(img)
        lbl_img.config(image=img)
        lbl_img.image = img
        btn_save.config(state=tk.NORMAL)
        lbl_path.config(text=file_path)

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, output_type=Output.STRING)
    return text

def save_to_excel():
    file_path = lbl_path.cget("text")
    if not file_path:
        return

    text = extract_text_from_image(file_path)
    lines = text.split('\n')
    data = [line.split() for line in lines if line]

    wb = openpyxl.Workbook()
    ws = wb.active

    for row_idx, row_data in enumerate(data):
        for col_idx, cell_value in enumerate(row_data):
            ws.cell(row=row_idx+1, column=col_idx+1, value=cell_value)

    excel_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if excel_file_path:
        wb.save(excel_file_path)
        lbl_status.config(text="Archivo Excel guardado exitosamente.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generar Excel con Imagen")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_select = tk.Button(frame, text="Seleccionar Imagen", command=select_image)
btn_select.grid(row=0, column=0, padx=5, pady=5)

lbl_img = tk.Label(frame)
lbl_img.grid(row=1, column=0, padx=5, pady=5)

lbl_path = tk.Label(frame, text="")
lbl_path.grid(row=2, column=0, padx=5, pady=5)

btn_save = tk.Button(frame, text="Guardar en Excel", state=tk.DISABLED, command=save_to_excel)
btn_save.grid(row=3, column=0, padx=5, pady=5)

lbl_status = tk.Label(frame, text="")
lbl_status.grid(row=4, column=0, padx=5, pady=5)

root.mainloop()
