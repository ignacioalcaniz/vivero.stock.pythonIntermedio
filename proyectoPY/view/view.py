from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog

# Crear ventana principal
vivero_stock = Tk()
vivero_stock.title("Vivero LaPlace Stock")

# Variables
var_nombre = StringVar()
var_cantidad = IntVar()
var_precio = StringVar()

# Labels y Entries
Label(vivero_stock, text="Nombre").grid(row=0, column=1, sticky=W)
Label(vivero_stock, text="Cantidad").grid(row=1, column=1, sticky=W)
Label(vivero_stock, text="Precio $").grid(row=2, column=1, sticky=W)

Entry(vivero_stock, textvariable=var_nombre).grid(row=0, column=2)
Entry(vivero_stock, textvariable=var_cantidad).grid(row=1, column=2)
Entry(vivero_stock, textvariable=var_precio).grid(row=2, column=2)

# Treeview
tree_vivero = ttk.Treeview(vivero_stock, columns=("col1", "col2", "col3"))
tree_vivero.column("#0", width=80, anchor=W)
tree_vivero.column("col1", width=150)
tree_vivero.column("col2", width=100)
tree_vivero.column("col3", width=100)

tree_vivero.heading("#0", text="ID")
tree_vivero.heading("col1", text="Nombre")
tree_vivero.heading("col2", text="Cantidad")
tree_vivero.heading("col3", text="Precio")

tree_vivero.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Exportar variables necesarias
__all__ = [
    "vivero_stock", "var_nombre", "var_cantidad", "var_precio", "tree_vivero"
]


