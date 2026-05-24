from PIL import Image, ImageTk
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
    # .strip() elimina espacios invisibles al inicio o final
    nombre = entry.get().strip()
    carpeta_ingresada = entry2.get().strip()

    # 1. Determinar qué directorio usar
    if carpeta_ingresada:
        ruta_base = carpeta_ingresada
        guardar_ruta(carpeta_ingresada)
    else:
        ruta_base = obtener_ruta_guardada()

    if not ruta_base:
        messagebox.showwarning("Atención", "Por favor, introduce la ruta del directorio.")
        return

    if not nombre:
        messagebox.showwarning("Atención", "Por favor, introduce el nombre de la imagen con su extensión.")
        return

    # 2. Convertir rutas relativas o con tilde (~) a rutas absolutas reales de Linux
    ruta_base = os.path.abspath(os.path.expanduser(ruta_base))
    
    # 3. Unir el directorio con el archivo
    ruta_archivo = os.path.join(ruta_base, nombre)

    # 4. Validar si el archivo existe de verdad en esa carpeta
    if not os.path.exists(ruta_archivo):
        messagebox.showerror("Error", f"No se encontró el archivo.\nRuta buscada:\n{ruta_archivo}")
        return

    try:
        img = Image.open(ruta_archivo)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen. ¿Seguro que es una imagen válida?\n{e}")
        return

    # 5. Procesar la extensión del archivo
    partes = nombre.split(".")
    if len(partes) < 2:
        messagebox.showwarning("Atención", "El archivo no tiene una extensión válida (ej: .png, .jpg).")
        return
    formato_original = partes[-1].lower()
    base = ".".join(partes[:-1])

    if formato == formato_original:
        messagebox.showinfo("Info", "La imagen ya tiene el formato seleccionado.")
        return

    # 6. Crear carpeta de salida dentro del mismo directorio
    carpeta_salida = os.path.join(ruta_base, "convertidos")
    os.makedirs(carpeta_salida, exist_ok=True)

    # 7. Guardar según el formato elegido
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
        messagebox.showwarning("Atención", "Por favor, selecciona un formato en el menú desplegable.")
        return

    messagebox.showinfo("Éxito", f"¡Conversión guardada en:\n{salida}")

# --- Interfaz Gráfica ---
app = customtkinter.CTk()
app.geometry("340x220")
app.title("LigtherConverter")

# Icono compatible Linux/Windows
if os.path.exists("icono.ico"):
    try:
        if os.name == 'nt':
            app.iconbitmap("icono.ico")
        else:
            img_icono = Image.open("icono.ico")
            photo = ImageTk.PhotoImage(img_icono)
            app.iconphoto(False, photo)
    except Exception:
        pass

app.resizable(False, False)
customtkinter.set_appearance_mode("dark")

# Primera Box: Nombre del archivo
entry = customtkinter.CTkEntry(app, placeholder_text="Nombre de la imagen (ej: foto.jpg)")
entry.pack(padx=20, pady=5, fill="x")

# Segunda Box: Directorio / Carpeta
entry2 = customtkinter.CTkEntry(app, placeholder_text="Ruta del directorio: ")
entry2.pack(padx=20, pady=5, fill="x")

# Auto-rellenar la segunda box si hay una ruta guardada previamente
ruta_inicial = obtener_ruta_guardada()
if ruta_inicial:
    entry2.insert(0, ruta_inicial)

# Menú y botón
optionmenu = customtkinter.CTkOptionMenu(app, values=["PNG", "JPG", "WEBP", "ICON"], command=optionmenu_callback)
optionmenu.set("Convertir a:")
optionmenu.pack(padx=20, pady=5)

button = customtkinter.CTkButton(app, text="Convertir", command=empezar_conversion)
button.pack(padx=20, pady=5)

app.mainloop()


