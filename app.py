
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
        self.espacio = tk.Frame(self.master, height=30, width=30)
        self.espacio.grid(row=0, column=0)
        self.text_sitio_web = tk.Label(self.master, text="Sitio Web:")
        self.text_sitio_web.grid(row=2, column=1)
        self.sitio_web = tk.Entry(self.master, width=15) #entrada web
        self.sitio_web.grid(row=2, column=2)
        self.text_usuario = tk.Label(self.master, text="Usuario:")
        self.text_usuario.grid(row=3, column=1)
        self.usuario = tk.Entry(self.master, width=15) #entrada usuario
        self.usuario.grid(row=3, column=2)
        self.text_contrasena = tk.Label(self.master, text="Contraseña:")
        self.text_contrasena.grid(row=4, column=1)
        self.contrasena = tk.Entry(self.master, width=15) #entrada contraseña
        self.contrasena.grid(row=4, column=2)
        self.boton_genera = tk.Button(self.master, text="Generar\nAleatoria", command=self.generar)
        self.boton_genera.grid(row=4, column=3)
        self.boton_agregar = tk.Button(self.master, text="Agregar", command=self.agregar)
        self.boton_agregar.grid(row=5, column=2)
        self.lista_sitios = tk.Listbox(self.master, width=20)
        self.lista_sitios.grid(row=6, column=2)
        self.boton_consulta = tk.Button(self.master, text="Consultar", command=self.consultar)
        self.boton_consulta.grid(row=7, column=1)
        self.boton_eliminar = tk.Button(self.master, text="Eliminar", command=self.eliminar)
        self.boton_eliminar.grid(row=7, column=3)

    def conexion(self):
        self.conn = sqlite3.connect("gestor.db")
        self.cursor = self.conn.cursor()

    def agregar(self):
        self.conexion()
        sql_insert = "INSERT INTO contraseñas (web, usuario, contraseña) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(sql_insert, (self.sitio_web.get(), self.usuario.get(), self.contrasena.get()))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Algo no salio bien {e}")
        self.conn.close()
        self.borrar_cajon()
        self.lista_sitios.insert(tk.END, self.sitio_web.get())

    def consultar(self):
        self.conexion()
        sql_select_all = "SELECT * FROM contraseñas"
        self.cursor.execute(sql_select_all)
        registros = self.cursor.fetchall()
        messagebox.showinfo("Informacion", f"Web:{registros[0]}\nUsuario:{registros[1]}\nContraseña:{registros[2]}")
        self.conn.close()

    def eliminar(self):
        self.conexion()
        sql_delete_condicional = "DELETE FROM contraseñas WHERE usuario = ?"
        try:
            self.cursor.execute(sql_delete_condicional, (self.lista_sitios.delete(tk.ACTIVE),))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Algo fallo {e}")
        self.conn.close()
        self.lista_sitios.delete(tk.ACTIVE)

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
        lista_caracteres = [chr(caracter) for caracter in range(ord("0"), ord("z")+1)]
        contrasena_ale = "".join(random.sample(lista_caracteres, 10))
        self.contrasena.insert(tk.END, contrasena_ale)

    def borrar_cajon(self):
        self.sitio_web.delete(0, tk.END)
        self.usuario.delete(0, tk.END)
        self.contrasena.delete(0, tk.END)






if __name__ == "__main__":
    root = tk.Tk()
    app = Gestor(root)
    root.mainloop()