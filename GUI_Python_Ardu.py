# Importar librerías
import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk, messagebox

# Variables globales
arduino = None

# Función para conectar al puerto seleccionado
def conectar_puerto():
    global arduino
    puerto = combo_puertos.get()
    if puerto:
        try:
            arduino = serial.Serial(port=puerto, baudrate=115200, timeout=0.1)
            messagebox.showinfo("Conexión", f"Conectado a {puerto}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar: {e}")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un puerto")

# Función para enviar un número y recibir la respuesta
def enviar_numero():
    global arduino
    if arduino:
        numero = entry_numero.get()
        if numero.isdigit():
            try:
                arduino.write(bytes(numero, 'utf-8'))
                time.sleep(0.05)
                data = arduino.readline().decode('utf-8').strip()
                etiqueta_resultado.config(text=f"Resultado: {data}")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al comunicar: {e}")
        else:
            messagebox.showwarning("Advertencia", "Ingrese un número válido")
    else:
        messagebox.showwarning("Advertencia", "Conéctese a un puerto primero")

# Función para listar los puertos disponibles
def listar_puertos():
    puertos = serial.tools.list_ports.comports()
    lista_puertos = [puerto.device for puerto in puertos]
    combo_puertos['values'] = lista_puertos

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz ESP32 - Python")
ventana.geometry("500x400")

# Widgets de la interfaz
frame = tk.Frame(ventana)
frame.pack(pady=20)

label_puerto = tk.Label(frame, text="Seleccione el puerto:")
label_puerto.grid(row=0, column=0, padx=5)

combo_puertos = ttk.Combobox(frame, state="readonly")
combo_puertos.grid(row=0, column=1, padx=5)

boton_listar = tk.Button(frame, text="Listar Puertos", command=listar_puertos)
boton_listar.grid(row=0, column=2, padx=5)

boton_conectar = tk.Button(ventana, text="Conectar", command=conectar_puerto)
boton_conectar.pack(pady=10)

entry_numero = tk.Label(ventana, text= "Ingrese un número:")
entry_numero.pack(pady=10)

entry_numero = tk.Entry(ventana)
entry_numero.pack(pady=10)

boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_numero)
boton_enviar.pack(pady=5)

etiqueta_resultado = tk.Label(ventana, text="Resultado: ")
etiqueta_resultado.pack(pady=10)

# Iniciar el loop de la interfaz
ventana.mainloop()
