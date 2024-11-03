<<<<<<< HEAD
import numpy as np
import tkinter as tk
from tkinter import Tk, Frame, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Hormiga import Hormiga  # Importa la clase Hormiga

# Crea una instancia de Hormiga y registra algunas iteraciones
hormiga = Hormiga([0, 0], [5, 5], 100, 0, 0, ["arriba", "derecha"], laberinto=[[None]])

# Ejemplo de 5 iteraciones; puedes cambiar este valor según necesites
for i in range(1, 6):  
    hormiga.registrar_iteracion(i)

# Obtener los datos para graficar
generaciones, puntos, tiempo = hormiga.obtener_datos()

# Configuración de la ventana principal
window = Tk()
window.geometry("800x700")

# Frame para la gráfica
frame = Frame(window, bg="blue")
frame.grid(column=0, row=0, sticky="nsew")

# Frame para el texto al lado de la gráfica
text_frame = Frame(window, bg="white")
text_frame.grid(column=1, row=0, sticky="nsew", padx=10, pady=10)

# Texto descriptivo en el frame lateral
Label(text_frame, text="Descripción de las gráficas:", font=("Arial", 14), bg="white").pack(anchor="nw", pady=5)
Label(text_frame, text="Gráfica 1: Muestra los puntos obtenidos por generación", font=("Arial", 13), wraplength=200, bg="white").pack(anchor="nw")
Label(text_frame, text="Gráfica 2: Muestra el tiempo tomado por cada generación", font=("Arial", 13), wraplength=200, bg="white").pack(anchor="nw")

# Crear la figura y ajustar el tamaño de las subplots para disposición vertical
fig, axs = plt.subplots(2, 1, dpi=70, figsize=(8, 10), sharex=True, facecolor="#00f9f844")
fig.suptitle("Estadísticas")

# Graficar los datos
axs[0].plot(generaciones, puntos, color="blue")
axs[0].set_title("Puntos por Generación")
axs[0].set_ylabel("Puntos")

axs[1].plot(generaciones, tiempo, color="blue")
axs[1].set_title("Tiempo por Generación")
axs[1].set_ylabel("Tiempo (s)")
axs[1].set_xlabel("Generación")

# Colocar el canvas en el frame
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")

# Iniciar el bucle principal de la ventana
window.mainloop()










=======
import numpy as np #esto no se puede usar
import tkinter as tk
from tkinter import Tk, Frame, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Hormiga import Hormiga  # Importa la clase Hormiga

# Crea una instancia de Hormiga y registra algunas iteraciones
hormiga = Hormiga([0, 0], [5, 5], 100, 0, 0, ["arriba", "derecha"], laberinto=[[None]])

# Ejemplo de 5 iteraciones; puedes cambiar este valor según necesites
for i in range(1, 6):  
    hormiga.registrar_iteracion(i)

# Obtener los datos para graficar
generaciones, puntos, tiempo = hormiga.obtener_datos()

# Configuración de la ventana principal
window = Tk()
window.geometry("800x700")

# Frame para la gráfica
frame = Frame(window, bg="blue")
frame.grid(column=0, row=0, sticky="nsew")

# Frame para el texto al lado de la gráfica
text_frame = Frame(window, bg="white")
text_frame.grid(column=1, row=0, sticky="nsew", padx=10, pady=10)

# Texto descriptivo en el frame lateral
Label(text_frame, text="Descripción de las gráficas:", font=("Arial", 14), bg="white").pack(anchor="nw", pady=5)
Label(text_frame, text="Gráfica 1: Muestra los puntos obtenidos por generación", font=("Arial", 13), wraplength=200, bg="white").pack(anchor="nw")
Label(text_frame, text="Gráfica 2: Muestra el tiempo tomado por cada generación", font=("Arial", 13), wraplength=200, bg="white").pack(anchor="nw")

# Crear la figura y ajustar el tamaño de las subplots para disposición vertical
fig, axs = plt.subplots(2, 1, dpi=70, figsize=(8, 10), sharex=True, facecolor="#00f9f844")
fig.suptitle("Estadísticas")

# Graficar los datos
axs[0].plot(generaciones, puntos, color="blue")
axs[0].set_title("Puntos por Generación")
axs[0].set_ylabel("Puntos")

axs[1].plot(generaciones, tiempo, color="blue")
axs[1].set_title("Tiempo por Generación")
axs[1].set_ylabel("Tiempo (s)")
axs[1].set_xlabel("Generación")

# Colocar el canvas en el frame
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")

# Iniciar el bucle principal de la ventana
window.mainloop()










>>>>>>> 9d1494c (Actualizacion 12:27)
