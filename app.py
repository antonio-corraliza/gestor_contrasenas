
import tkinter as tk
from tkinter import messagebox
import random
import sqlite3

class Gestor:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor contraseñas")
        self.master.geometry("300x400")
        self.widgets()
        

    def widgets(self):
        espacio = tk.Frame(self.master, height=30, width=30)
        espacio.grid(row=0, column=0)
        text_sitio_web = tk.Label(self.master, text="Sitio Web:")
        text_sitio_web.grid(row=2, column=1)
        sitio_web = tk.Entry(self.master, width=15)
        sitio_web.grid(row=2, column=2)
        text_usuario = tk.Label(self.master, text="Usuario:")
        text_usuario.grid(row=3, column=1)
        usuario = tk.Entry(self.master, width=15)
        usuario.grid(row=3, column=2)
        text_contrasena = tk.Label(self.master, text="Contraseña:")
        text_contrasena.grid(row=4, column=1)
        contrasena = tk.Entry(self.master, width=15)
        contrasena.grid(row=4, column=2)
        boton_genera = tk.Button(self.master, text="Generar\nAleatoria")
        boton_genera.grid(row=4, column=3)
        boton_agregar = tk.Button(self.master, text="Agregar")
        boton_agregar.grid(row=5, column=2)
        lista_sitios = tk.Listbox(self.master, width=20)
        lista_sitios.grid(row=6, column=2)
        boton_consulta = tk.Button(self.master, text="Consultar")
        boton_consulta.grid(row=7, column=1)
        boton_eliminar = tk.Button(self.master, text="Eliminar")
        boton_eliminar.grid(row=7, column=3)

    def conexion(self):
        self.conn = sqlite3.connect("gestor.db")
        self.cursor = self.conn.cursor()

    def agregar(self):
        self.conexion()
        self.cursor.execute()
        self.conn.commit()
        self.conn.close()

    def consultar(self):
        self.conexion()
        self.cursor.execute()
        self.conn.commit()
        self.conn.close()

    def eliminar(self):
        self.conexion()
        self.cursor.execute()
        self.conn.commit()
        self.conn.close()

    def tablas(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS contraseñas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            web TEXT NOT NULL,
            usuario TEXT NOT NULL,
            contraseña TEXT NOT NULL
        );
        """
        self.conexion()
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        self.conn.close()

    def generar(self):
        pass








if __name__ == "__main__":
    root = tk.Tk()
    app = Gestor(root)
    root.mainloop()