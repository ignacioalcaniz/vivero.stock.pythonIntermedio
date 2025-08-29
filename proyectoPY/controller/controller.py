"""
Módulo controller
-----------------

Este módulo define la clase ViveroController, que actúa como el controlador en la arquitectura MVC 
(Modelo-Vista-Controlador) de la aplicación "Vivero La Place Stock".

Responsabilidades del controlador:
- Coordinar la comunicación entre la vista (interfaz gráfica) y el modelo (base de datos).
- Validar datos ingresados por el usuario.
- Ejecutar las operaciones CRUD sobre la base de datos.
- Actualizar la interfaz según los cambios.
- Manejar errores y mostrar mensajes al usuario.
"""

from tkinter import Button, Menu, messagebox, filedialog
from proyectoPY.view.view import vivero_stock, var_nombre, var_cantidad, var_precio, tree_vivero
from proyectoPY.model.model import ProductoModel
import re


class ViveroController:
    """
    Controlador principal de la aplicación.

    Maneja las acciones del usuario desde la interfaz gráfica, valida datos,
    invoca los métodos del modelo y actualiza la vista.

    Métodos principales:
    - guardar: Inserta un nuevo producto validado en la base de datos.
    - eliminar: Elimina un producto seleccionado.
    - modificar: Modifica los datos de un producto existente.
    - consultar: Carga los datos del producto seleccionado en los campos de entrada.
    - guardar_en_archivo: Exporta los productos a un archivo CSV.
    - limpiar_campos: Limpia los campos de entrada después de guardar o modificar.
    """

    def __init__(self):
        """
        Inicializa el controlador, configura botones, menú y carga los productos en el Treeview.
        """
        self.model = ProductoModel()
        self.configurar_botones()
        self.configurar_menu()
        self.actualizar_treeview()

    def configurar_botones(self):
        """
        Configura los botones de la interfaz gráfica y sus comandos asociados.
        """
        Button(vivero_stock, text="Guardar", command=self.guardar, bg="green", fg="white").grid(row=3, column=0, padx=5, pady=5)
        Button(vivero_stock, text="Eliminar", command=self.eliminar, bg="red", fg="white").grid(row=3, column=1, padx=5, pady=5)
        Button(vivero_stock, text="Modificar", command=self.modificar, bg="yellow", fg="black").grid(row=3, column=2, padx=5, pady=5)
        Button(vivero_stock, text="Consultar", command=self.consultar, bg="blue", fg="white").grid(row=3, column=3, padx=5, pady=5)

    def configurar_menu(self):
        """
        Configura la barra de menú superior con opciones para guardar en archivo y salir.
        """
        menu_bar = Menu(vivero_stock)
        archivo_menu = Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Guardar como", command=self.guardar_en_archivo)
        archivo_menu.add_command(label="Salir", command=vivero_stock.quit)
        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        vivero_stock.config(menu=menu_bar)

    def actualizar_treeview(self):
        """
        Actualiza el contenido del Treeview con los datos actuales de la base de datos.
        """
        for item in tree_vivero.get_children():
            tree_vivero.delete(item)
        try:
            productos = self.model.obtener_productos()
            for prod in productos:
                tree_vivero.insert("", "end", text=prod[0], values=(prod[1], prod[2], prod[3]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los productos:\n{e}")

    def guardar(self):
        """
        Guarda un nuevo producto en la base de datos después de validar los campos.
        Valida el nombre usando una expresión regular.
        """
        nombre = var_nombre.get()
        cantidad = var_cantidad.get()
        precio = var_precio.get()

        if not re.fullmatch(r"^[A-Za-z]+(?:[ _-][A-Za-z]+)*$", nombre):
            messagebox.showwarning("Nombre inválido", "El nombre debe contener solo letras y ser alfanumérico.")
            return

        if nombre == "" or precio == "":
            messagebox.showwarning("Faltan datos", "Complete todos los campos.")
            return

        try:
            self.model.insertar_producto(nombre, cantidad, precio)
            messagebox.showinfo("Guardado", "Producto guardado exitosamente.")
            self.limpiar_campos()
            self.actualizar_treeview()
        except Exception as e:
            messagebox.showerror("Error al guardar", f"Ocurrió un error al guardar:\n{e}")

    def eliminar(self):
        """
        Elimina el producto seleccionado en el Treeview de la base de datos.
        """
        seleccionado = tree_vivero.focus()
        if seleccionado:
            id_producto = tree_vivero.item(seleccionado, "text")
            try:
                self.model.eliminar_producto(id_producto)
                messagebox.showinfo("Eliminado", "Producto eliminado.")
                self.actualizar_treeview()
            except Exception as e:
                messagebox.showerror("Error al eliminar", f"No se pudo eliminar el producto:\n{e}")
        else:
            messagebox.showwarning("Seleccionar", "Seleccione un producto para eliminar.")

    def modificar(self):
        """
        Modifica los datos del producto seleccionado con los nuevos valores ingresados.
        """
        seleccionado = tree_vivero.focus()
        if seleccionado:
            id_producto = tree_vivero.item(seleccionado, "text")
            nombre = var_nombre.get()
            cantidad = var_cantidad.get()
            precio = var_precio.get()

            if nombre == "" or precio == "":
                messagebox.showwarning("Faltan datos", "Complete todos los campos.")
                return

            try:
                self.model.modificar_producto(id_producto, nombre, cantidad, precio)
                messagebox.showinfo("Modificado", "Producto modificado correctamente.")
                self.actualizar_treeview()
            except Exception as e:
                messagebox.showerror("Error al modificar", f"No se pudo modificar el producto:\n{e}")
        else:
            messagebox.showwarning("Seleccionar", "Seleccione un producto para modificar.")

    def consultar(self):
        """
        Carga los datos del producto seleccionado en los campos de entrada para su consulta.
        """
        seleccionado = tree_vivero.focus()
        if seleccionado:
            nombre, cantidad, precio = tree_vivero.item(seleccionado, "values")
            var_nombre.set(nombre)
            var_cantidad.set(cantidad)
            var_precio.set(precio)
        else:
            messagebox.showwarning("Seleccionar", "Seleccione un producto para consultar.")

    def guardar_en_archivo(self):
        """
        Exporta todos los productos mostrados en el Treeview a un archivo CSV.
        """
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            try:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write("ID,Nombre,Cantidad,Precio\n")
                    for item in tree_vivero.get_children():
                        id_val = tree_vivero.item(item, "text")
                        nombre, cantidad, precio = tree_vivero.item(item, "values")
                        f.write(f"{id_val},{nombre},{cantidad},{precio}\n")
                messagebox.showinfo("Guardado", f"Datos exportados correctamente a:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error al exportar", f"No se pudo guardar el archivo:\n{e}")

    def limpiar_campos(self):
        """
        Limpia los campos de entrada (nombre, cantidad, precio) luego de una operación.
        """
        var_nombre.set("")
        var_cantidad.set(0)
        var_precio.set("")


# ---------- Inicio del programa ----------
if __name__ == "__main__":
    app = ViveroController()
    vivero_stock.mainloop()



