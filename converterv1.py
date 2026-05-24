from PIL import Image
import os
import customtkinter
import tkinter
from tkinter import messagebox

ARCHIVO_RUTA = "propiedades_de_ruta.txt"
formato = None

def optionmenu_callback(choice):
    global formato
    formato = choice.lower()

def obtener_ruta_guardada():
    """Lee la ruta guardada en el archivo, si existe."""
    if os.path.exists(ARCHIVO_RUTA):
        with open(ARCHIVO_RUTA, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def guardar_ruta(carpeta):
    """Guarda la ruta en el archivo."""
    with open(ARCHIVO_RUTA, "w", encoding="utf-8") as f:
        f.write(carpeta.strip())

def empezar_conversion():
    global formato
    nombre = entry.get().strip()
    carpeta = entry2.get().strip()

    # Si el usuario escribió una ruta nueva, la guardamos
    if carpeta:
        guardar_ruta(carpeta)

    # Usamos la ruta guardada
    ruta_base = obtener_ruta_guardada()
    if not ruta_base:
        messagebox.showwarning("Atención", "No hay ruta guardada. Escribe una carpeta primero.")
        return

    ruta = os.path.join(ruta_base, nombre)

    if not os.path.exists(ruta):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}")
        return

    img = Image.open(ruta)

    partes = nombre.split(".")
    if len(partes) < 2:
        messagebox.showwarning("Atención", "El archivo no tiene extensión.")
        return
    formato_original = partes[-1].lower()
    base = ".".join(partes[:-1])

    if formato == formato_original:
        messagebox.showinfo("Info", "Estás intentando convertir al mismo formato.")
        return

    carpeta_salida = os.path.join(ruta_base, "convertidos")
    os.makedirs(carpeta_salida, exist_ok=True)

    if formato == "png":
        salida = os.path.join(carpeta_salida, f"{base}.png")
        img.save(salida, "PNG")
    elif formato in ("jpg", "jpeg"):
        img = img.convert("RGB")
        salida = os.path.join(carpeta_salida, f"{base}.jpg")
        img.save(salida, "JPEG")
    elif formato == "webp":
        salida = os.path.join(carpeta_salida, f"{base}.webp")
        img.save(salida, "WEBP")
    elif formato == "icon":
        salida = os.path.join(carpeta_salida, f"{base}.ico")
        img.save(salida, "ICO")
    else:
        messagebox.showwarning("Atención", f"Formato no soportado: {formato}")
        return

    messagebox.showinfo("Éxito", f"Conversión completa:\n{salida}")

# Interfaz
app = customtkinter.CTk()
app.geometry("340x180")
app.title("LigtherConverter")
app.iconbitmap("icono.ico")
app.resizable(False, False)
customtkinter.set_appearance_mode("dark")

optionmenu = customtkinter.CTkOptionMenu(app, values=["PNG", "JPG", "WEBP", "ICON"],
                                         command=optionmenu_callback)
optionmenu.set("Convertir a:")

entry = customtkinter.CTkEntry(app, placeholder_text="archivo (ej: foto.png)")
entry2 = customtkinter.CTkEntry(app, placeholder_text="ruta de archivos:")

button = customtkinter.CTkButton(app, text="Convertir", command=empezar_conversion)

entry.pack(padx=20, pady=5, fill="x")
entry2.pack(padx=20, pady=5, fill="x")
optionmenu.pack(padx=20, pady=5)
button.pack(padx=20, pady=5)

app.mainloop()
