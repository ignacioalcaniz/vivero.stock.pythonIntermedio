import sqlite3


class ProductoModel:
    """
    Clase modelo para manejar la base de datos de productos.

    Métodos:
        crear_tabla(): Crea la tabla 'productos' si no existe.
        obtener_productos(): Devuelve todos los productos como lista de tuplas.
        insertar_producto(nombre, cantidad, precio): Inserta un nuevo producto.
        eliminar_producto(id_producto): Elimina un producto por su ID.
        modificar_producto(id_producto, nombre, cantidad, precio): Modifica un producto existente.
    """

    def __init__(self, db_name="viverolaplace.db"):
        """
        Inicializa la clase con la base de datos y crea la tabla si no existe.
        """
        self.db_name = db_name
        self.crear_tabla()

    def conectar(self):
        """
        Establece y retorna una conexión a la base de datos.
        """
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        """
        Crea la tabla de productos si no existe.
        """
        try:
            con = self.conectar()
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    cantidad INTEGER,
                    precio TEXT
                )
            """)
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] al crear la tabla: {e}")
        finally:
            con.close()

    def obtener_productos(self):
        """
        Obtiene todos los productos de la base de datos.

        Returns:
            list: Lista de tuplas con los productos.
        """
        try:
            con = self.conectar()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY id ASC")
            productos = cursor.fetchall()
            return productos
        except sqlite3.Error as e:
            print(f"[ERROR] al obtener productos: {e}")
            return []
        finally:
            con.close()

    def insertar_producto(self, nombre, cantidad, precio):
        """
        Inserta un nuevo producto en la base de datos.

        Args:
            nombre (str): Nombre del producto.
            cantidad (int): Cantidad en stock.
            precio (str): Precio del producto.
        """
        try:
            con = self.conectar()
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO productos(nombre, cantidad, precio) VALUES (?, ?, ?)",
                (nombre, cantidad, precio)
            )
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] al insertar producto: {e}")
        finally:
            con.close()

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto por su ID.

        Args:
            id_producto (int): ID del producto a eliminar.
        """
        try:
            con = self.conectar()
            cursor = con.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] al eliminar producto: {e}")
        finally:
            con.close()

    def modificar_producto(self, id_producto, nombre, cantidad, precio):
        """
        Modifica un producto existente.

        Args:
            id_producto (int): ID del producto.
            nombre (str): Nuevo nombre.
            cantidad (int): Nueva cantidad.
            precio (str): Nuevo precio.
        """
        try:
            con = self.conectar()
            cursor = con.cursor()
            cursor.execute(
                "UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
                (nombre, cantidad, precio, id_producto)
            )
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] al modificar producto: {e}")
        finally:
            con.close()

