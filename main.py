# -*- coding: utf-8 -*- # Permite usar caracteres como tildes o la "ñ".
import tkinter as tk # Carga las herramientas para crear la ventana.
from tkinter import messagebox # Importa las alertas emergentes (ventanas de error).
from logic import Usuario, ReservaSala # Importamos las clases del archivo logic.py

class App: # Estructura principal que controla todo el programa.
    def __init__(self, root): # Configuración inicial al abrir el programa.
        self.root = root # Guarda la ventana principal en la memoria de la clase.
        self.root.title("Study Room System") # Escribe el nombre en la parte superior de la ventana.
        self.root.geometry("400x500") # Define el ancho y largo de la ventana en píxeles.
        
        self.auth = Usuario() # Crea el objeto que validará el login.
        self.reservations = [] # Lista para almacenar las reservas
        self.show_login() # Ordena mostrar la pantalla de inicio de sesión de inmediato.

    def clear(self): # Borra todo lo que hay en la ventana para dibujar algo nuevo.
        for w in self.root.winfo_children(): w.destroy() # Busca cada botón o texto y lo elimina uno por uno.

    def show_login(self): # Dibuja los elementos del formulario de acceso.
        self.clear()
        tk.Label(self.root, text="LOGIN SYSTEM", font=("Arial", 14, "bold")).pack(pady=20) # Muestra el título principal en negrita.
        
        tk.Label(self.root, text="Username:").pack()
        self.u_ent = tk.Entry(self.root) # Crea el cuadro para escribir el nombre de usuario.
        self.u_ent.pack() 
        
        tk.Label(self.root, text="Password:").pack()
        self.p_ent = tk.Entry(self.root, show="*") # Crea el cuadro de contraseña ocultando los caracteres con asteriscos.
        self.p_ent.pack()
        
        tk.Button(self.root, text="Login", command=self.process_login).pack(pady=20) # Crea el botón que activa la validación al hacer clic.

    def process_login(self): # Lógica que decide si entras o no al sistema.
        if self.auth.validar(self.u_ent.get(), self.p_ent.get()): # Valida contra la clase Usuario
            self.show_main() # Si los datos son correctos, abre el gestor de reservas.
        else:
            messagebox.showerror("Error", "Invalid credentials") # Si fallan, muestra una ventana de "Acceso Denegado".

    def show_main(self): # Crea la interfaz del Ejercicio 2 en idioma inglés.
        self.clear()
        tk.Label(self.root, text="RESERVATIONS MANAGER", font=("Arial", 12)).pack(pady=10)
        
        # Campos de entrada
        tk.Label(self.root, text="Student Name:").pack()
        self.name_in = tk.Entry(self.root) # Cuadro para el nombre del estudiante responsable.
        self.name_in.pack()
        
        tk.Label(self.root, text="Hourly Rate:").pack()
        self.rate_in = tk.Entry(self.root) # Cuadro para ingresar el precio por hora.
        self.rate_in.pack()
        
        tk.Label(self.root, text="Start Time:").pack()
        self.start_in = tk.Entry(self.root) # Cuadro para anotar la hora de inicio.
        self.start_in.pack()
        
        tk.Button(self.root, text="Create Reservation", command=self.add_res).pack(pady=10)
        
        # Lista visual
        self.lb = tk.Listbox(self.root, width=40) # Cuadro blanco que lista las reservas creadas.
        self.lb.pack(pady=10)
        
        tk.Label(self.root, text="End Time:").pack()
        self.end_in = tk.Entry(self.root) # Cuadro para anotar la hora de entrega de la sala.
        self.end_in.pack()
        
        tk.Button(self.root, text="Finish & Calculate", command=self.finish).pack(pady=10) #prueba de git

        tk.Label(self.root, text="Created by Fredy Tangarife - UNAD Student").pack() # Créditos del autor en la parte inferior.

    def add_res(self): # Proceso para crear una nueva reserva.
        try:
            r = ReservaSala(self.name_in.get(), self.rate_in.get()) # Crea instancia de ReservaSala
            r.registrar_inicio(self.start_in.get())
            self.reservations.append(r) # Guarda la reserva en la base de datos temporal.
            self.lb.insert(tk.END, f"Res: {r.obtener_usuario()}") # Agrega el nombre del usuario a la lista visual.
        except:
            messagebox.showwarning("Warning", "Invalid input data")

    def finish(self): # Proceso para liquidar y cobrar la reserva.
        select = self.lb.curselection() # Detecta qué reserva elegiste con el ratón.
        if select:
            res = self.reservations[select[0]]
            try:
                cost = res.calcular_costo(self.end_in.get()) # Llama a la lógica para obtener el precio final.
                messagebox.showinfo("Result", f"User: {res.obtener_usuario()}\nTotal: ${cost:.2f}") # Muestra el total a pagar en una ventana informativa.
            except:
                messagebox.showerror("Error", "Check End Time") # Muestra una ventana informativa si hay un error con el tiempo final.

if __name__ == "__main__": # Evita que el código se ejecute solo al ser importado.
    root = tk.Tk() # Inicia el motor principal de la interfaz gráfica.
    app = App(root) # Inicia tu aplicación dentro del motor de Windows.
    root.mainloop() # Mantiene el programa abierto y atento a tus clics.