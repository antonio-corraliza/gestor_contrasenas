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
        self.cargar_listbox()
        
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
        self.lista_sitios = tk.Listbox(self.master, width=20, selectmode=tk.SINGLE)
        self.lista_sitios.grid(row=6, column=2)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.lista_sitios.yview)
        self.scrollbar.grid(row=6, column=3)
        self.lista_sitios.config(yscrollcommand=self.scrollbar.set)
        self.boton_consulta = tk.Button(self.master, text="Consultar", command=self.consultar)
        self.boton_consulta.grid(row=7, column=1)
        self.boton_eliminar = tk.Button(self.master, text="Eliminar", command=self.eliminar)
        self.boton_eliminar.grid(row=7, column=3)

    def conexion(self):
        self.conn = sqlite3.connect("gestor.db")
        self.cursor = self.conn.cursor()

    def agregar(self):
        # Validar campos vacíos
        if not self.sitio_web.get() or not self.usuario.get() or not self.contrasena.get():
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        usuario_cifrado = self.cifrado(self.usuario.get())
        contrasena_cifrada = self.cifrado(self.contrasena.get())

        self.conexion()
        sql_insert = """
            INSERT INTO contraseñas (web, usuario, contraseña)
            VALUES (?, ?, ?)
            ON CONFLICT(web) DO UPDATE SET
                usuario=excluded.usuario,
                contraseña=excluded.contraseña
        """
        try:
            self.cursor.execute(sql_insert, (self.sitio_web.get(), usuario_cifrado, contrasena_cifrada))
            self.conn.commit()
            messagebox.showinfo("Actualización", "Los datos han sido agregados o actualizados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Algo no salió bien: {e}")
        self.conn.close()

        # Limpiar y recargar el Listbox para evitar duplicados
        self.lista_sitios.delete(0, tk.END)
        self.cargar_listbox()

        self.sitio_web.delete(0, tk.END)
        self.usuario.delete(0, tk.END)
        self.contrasena.delete(0, tk.END)


    def consultar(self):
        seleccion = self.lista_sitios.curselection()
        if not seleccion:
            messagebox.showwarning("Selecciona un sitio", "Por favor, selecciona un sitio de la lista.")
            return

        sitio = self.lista_sitios.get(seleccion[0])

        self.conexion()
        sql_select = "SELECT web, usuario, contraseña FROM contraseñas WHERE web = ?"
        self.cursor.execute(sql_select, (sitio,))
        registro = self.cursor.fetchone()
        self.conn.close()

        if registro:
            usuario_descifrado = self.descifrado(registro[1])
            contrasena_descifrada = self.descifrado(registro[2])
            messagebox.showinfo("Información", f"Web: {registro[0]}\nUsuario: {usuario_descifrado}\nContraseña: {contrasena_descifrada}")
        else:
            messagebox.showwarning("No encontrado", "No se encontró el registro seleccionado.")

    def eliminar(self):
        respuesta = messagebox.askquestion("Confirmar eliminación", "¿Estás seguro de que quieres eliminar este sitio?")
        if respuesta != "yes":
            return

        seleccion = self.lista_sitios.curselection()
        if not seleccion:
            messagebox.showwarning("Selecciona un sitio", "Por favor, selecciona un sitio de la lista.")
            return

        sitio = self.lista_sitios.get(seleccion[0])

        self.conexion()
        sql_delete = "DELETE FROM contraseñas WHERE web = ?"
        try:
            self.cursor.execute(sql_delete, (sitio,))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Algo falló: {e}")
        self.conn.close()

        self.lista_sitios.delete(seleccion[0])

    def tablas(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS contraseñas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            web TEXT NOT NULL UNIQUE,
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
        contrasena_ale = "".join(random.sample(lista_caracteres, 12))
        self.contrasena.delete(0, tk.END)
        self.contrasena.insert(tk.END, contrasena_ale)

    def cargar_listbox(self):
        self.lista_sitios.delete(0, tk.END)  # Limpia el Listbox antes de cargar
        self.conexion()
        try:
            self.cursor.execute("SELECT web FROM contraseñas")
            filas = self.cursor.fetchall()
            for fila in filas:
                self.lista_sitios.insert(tk.END, fila[0])
        except Exception as e:
            messagebox.showerror("Error", f"Algo fallo:{e}")
        self.conn.close() 

    def cifrado(self, texto, desplazamiento=3):
        resultado = ""
        for char in texto:
            resultado += chr((ord(char) + desplazamiento) % 256)  # 256 para cubrir todos los caracteres ASCII extendidos
        return resultado

    def descifrado(self, texto, desplazamiento=3):
        resultado = ""
        for char in texto:
            resultado += chr((ord(char) - desplazamiento) % 256)
        return resultado

    def contra_maestra(self):
        pass





if __name__ == "__main__":
    root = tk.Tk()
    app = Gestor(root)
    root.mainloop()