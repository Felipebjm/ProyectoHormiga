import tkinter as tk
from tkinter import ttk

class Laberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Hormiga en Laberinto")
        self.matriz = []
        
        # Diccionario de letras para representar ítems y sus colores
        self.items_letras = {
            "azúcar": ("A", "lightblue"),
            "vino": ("V", "brown4"),
            "veneno": ("VN", "purple3"),
            "roca": ("R", "chocolate3"),
        }

        # Variable para almacenar el ítem seleccionado
        self.selected_item = tk.StringVar(value="azúcar")

        self.hormiga_pos = None  # Inicia sin posición definida
        self.seleccionar_tamano_matriz()

    def seleccionar_tamano_matriz(self):
        # Selector de tamaño de matriz
        self.size_frame = ttk.LabelFrame(self.root, text="Tamaño de la Matriz")
        self.size_frame.pack(pady=10)

        tk.Label(self.size_frame, text="Filas:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_var = tk.IntVar(value=5)
        self.rows_spinner = tk.Spinbox(self.size_frame, from_=3, to=10, textvariable=self.rows_var, width=5)
        self.rows_spinner.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.size_frame, text="Columnas:").grid(row=0, column=2, padx=5, pady=5)
        self.cols_var = tk.IntVar(value=5)
        self.cols_spinner = tk.Spinbox(self.size_frame, from_=3, to=10, textvariable=self.cols_var, width=5)
        self.cols_spinner.grid(row=0, column=3, padx=5, pady=5)

        self.apply_size_button = ttk.Button(self.size_frame, text="Aplicar Tamaño", command=self.limpiar_cuadricula)
        self.apply_size_button.grid(row=1, column=0, columnspan=4, pady=10)

        # Menú de selección de ítem
        self.item_selector_frame = ttk.LabelFrame(self.root, text="Seleccionar Ítem")
        self.item_selector_frame.pack(pady=10)

        for item_name in self.items_letras:
            radio_button = ttk.Radiobutton(
                self.item_selector_frame, text=item_name.capitalize(),
                variable=self.selected_item, value=item_name
            )
            radio_button.pack(anchor="w")

        # Contenedor para el laberinto
        self.grid_frame = ttk.Frame(self.root)
        self.grid_frame.pack(pady=10)

    def limpiar_cuadricula(self):
        # Limpiar la cuadrícula existente
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        rows, cols = self.rows_var.get(), self.cols_var.get()
        self.matriz = [[None for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                label = tk.Label(
                    self.grid_frame, width=2, height=1,
                    bg="white", relief="solid", borderwidth=1,
                    font=("Arial", 20)
                )
                label.grid(row=i, column=j, padx=0, pady=0)
                label.bind("<Button-1>", lambda e, x=i, y=j: self.agregar_item(x, y))
                label.bind("<Button-3>", lambda e, x=i, y=j: self.set_hormiga_position(x, y))
                self.matriz[i][j] = label

    def agregar_item(self, row, col):
        # Obtener el ítem seleccionado y asignar su letra al label
        selected_item = self.selected_item.get()
        if selected_item in self.items_letras:
            item_letter, item_color = self.items_letras[selected_item]
            self.matriz[row][col].config(text=item_letter, bg=item_color)
            print(f"Objeto '{selected_item}' agregado en posición ({row}, {col})")

    def set_hormiga_position(self, row, col):
        # Establecer la posición inicial de la hormiga sin notificación
        if self.hormiga_pos is not None:
            old_row, old_col = self.hormiga_pos
            self.matriz[old_row][old_col].config(text="", bg="white")

        self.hormiga_pos = (row, col)
        self.matriz[row][col].config(text="H", bg="yellow")
        print(f"Hormiga colocada en posición ({row}, {col})")

# Código para inicializar Tkinter y crear el laberinto
if __name__ == "__main__":
    root = tk.Tk()
    laberinto = Laberinto(root)
    root.mainloop()














