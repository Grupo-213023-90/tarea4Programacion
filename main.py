"""
Módulo: main.py
Descripción: Punto de entrada principal de la aplicación. 
Contiene la interfaz gráfica (GUI) construida con Tkinter y actúa como 
orquestador, uniendo las clases de entidades.py, servicios.py, logica.py y excepciones.py
Maneja las excepciones para asegurar que el sistema no colapse.
Fase 5: Integración y Pruebas.
Autor: Fredy Andrés Tangarife Correa
Descripción 2: Implementa la gestión de datos en memoria mediante listas y 
una simulación automatizada de 10 casos de prueba.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Importaciones de los módulos desarrollados en fases anteriores
try:
    from entidades import Cliente
    from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
    from logica import Reserva, SistemaLog
    from excepciones import DatosInvalidosError, SoftwareFJError
except ImportError as e:
    print(f"Error de dependencias: {e}")
    sys.exit()

class AppSoftwareFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ: Integración y Pruebas")
        self.root.geometry("600x750")
        
        # --- FASE 5: GESTIÓN EN MEMORIA ---
        # Listas para persistencia temporal durante la ejecución
        self.lista_clientes = []
        self.lista_servicios = []
        self.lista_reservas = []
        
        self._crear_interfaz()
        SistemaLog.registrar("Sistema iniciado - Fase de Integración y Pruebas.")

    def _crear_interfaz(self):
        """Construye la interfaz gráfica y añade el botón de simulación."""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Campos de entrada (Iguales a las fases anteriores)
        ttk.Label(main_frame, text="DATOS DEL CLIENTE", font=("Arial", 11, "bold")).pack(pady=5)
        self.ent_nombre = self._crear_campo(main_frame, "Nombre Completo:")
        self.ent_doc = self._crear_campo(main_frame, "Documento:")
        self.ent_correo = self._crear_campo(main_frame, "Correo Electrónico:")

        ttk.Label(main_frame, text="DETALLES DEL SERVICIO", font=("Arial", 11, "bold")).pack(pady=10)
        self.combo_servicio = ttk.Combobox(main_frame, state="readonly", 
                                          values=["Reserva de Sala", "Alquiler de Equipo", "Asesoría Especializada"])
        self.combo_servicio.pack(fill="x", pady=2)
        self.combo_servicio.current(0)
        
        self.ent_valor_base = self._crear_campo(main_frame, "Valor Unitario ($):")
        self.ent_cant = self._crear_campo(main_frame, "Cantidad:")

        # --- BOTONES DE ACCIÓN ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="REGISTRAR MANUAL", command=self.procesar_datos).pack(side=tk.LEFT, padx=5)
        
        # Nuevo botón para la Fase 5
        ttk.Button(btn_frame, text="EJECUTAR 10 PRUEBAS", command=self.ejecutar_simulacion).pack(side=tk.LEFT, padx=5)

        # Log de salida
        self.txt_output = tk.Text(main_frame, height=15, font=("Consolas", 9), state="disabled", bg="#f4f4f4")
        self.txt_output.pack(fill="both", expand=True)

    def _crear_campo(self, parent, label_text):
        """Método auxiliar para generar etiquetas y entradas rápidamente."""
        ttk.Label(parent, text=label_text).pack(anchor="w")
        entry = ttk.Entry(parent)
        entry.pack(fill="x", pady=2)
        return entry

    def procesar_datos(self):
        """Procesa una operación manual y la guarda en las listas de memoria."""
        try:
            # Captura de datos
            reserva = self._crear_objeto_reserva(
                self.ent_nombre.get(), 
                self.ent_doc.get(), 
                self.ent_correo.get(),
                self.combo_servicio.get(),
                self.ent_valor_base.get(),
                self.ent_cant.get()
            )
            
            # Confirmación y almacenamiento
            confirmacion = reserva.confirmar_reserva()
            
            if reserva.confirmada:
                # Almacenamos los objetos en las listas (Gestión en Memoria)
                self.lista_clientes.append(reserva.cliente)
                self.lista_servicios.append(reserva.servicio)
                self.lista_reservas.append(reserva)
                
                self._actualizar_log(reserva.generar_comprobante())
                messagebox.showinfo("Éxito", confirmacion)
            else:
                messagebox.showwarning("Atención", confirmacion)

        except SoftwareFJError as e:
            messagebox.showwarning("Error de Negocio", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Fallo: {e}")

    def _crear_objeto_reserva(self, nom, doc, mail, tipo, val, cant):
        """Lógica de instanciación modularizada para ser usada por manual y simulación."""
        if not all([nom, doc, mail, val, cant]):
            raise DatosInvalidosError("Existen campos vacíos.")
        
        cli = Cliente(nom, doc, mail)
        
        if tipo == "Reserva de Sala":
            srv = ReservaSala("S-101", int(cant), float(val))
        elif tipo == "Alquiler de Equipo":
            srv = AlquilerEquipo("E-202", int(cant), float(val))
        else:
            srv = AsesoriaEspecializada("A-303", int(cant), float(val))
            
        return Reserva(cli, srv)

    # --- FASE 5: SIMULACIÓN DE 10 OPERACIONES ---
    def ejecutar_simulacion(self):
        """
        Ejecuta 10 casos de prueba predefinidos (exitosos y fallidos).
        Asegura que el programa no se detenga ante errores graves.
        """
        casos = [
            ("Juan Perez", "12345", "juan@mail.com", "Reserva de Sala", "50000", "2"),     # OK
            ("Ana", "54321", "ana@mail.com", "Alquiler de Equipo", "30000", "6"),        # Error: Nombre corto
            ("Carlos Ruiz", "abcde", "carlos@mail.com", "Asesoría Especializada", "80000", "3"), # Error: Doc no numérico
            ("Marta Gomez", "99887", "marta@gmail.com", "Reserva de Sala", "0", "4"),      # Error: Costo cero
            ("Luis T.", "11223", "luis@mail.com", "Alquiler de Equipo", "25000", "10"),    # OK (Descuento)
            ("Sonia", "44556", "sonia.com", "Asesoría Especializada", "60000", "1"),       # Error: Mail inválido
            ("Fredy Tangarife", "77889", "fredy@unad.edu.co", "Asesoría Especializada", "90000", "5"), # OK (Recargo)
            ("", "00000", "vacio@mail.com", "Reserva de Sala", "10000", "1"),              # Error: Vacío
            ("Elena Mar", "33445", "elena@mail.com", "Alquiler de Equipo", "45000", "2"),  # OK
            ("Roberto", "66778", "rob@mail.com", "Reserva de Sala", "55000", "3")          # OK
        ]

        self._actualizar_log("--- INICIANDO SIMULACIÓN DE 10 CASOS ---\n")
        exitos = 0
        fallos = 0

        for i, (n, d, m, t, v, c) in enumerate(casos, 1):
            try:
                res = self._crear_objeto_reserva(n, d, m, t, v, c)
                log_res = res.confirmar_reserva()
                
                if res.confirmada:
                    exitos += 1
                    self.lista_reservas.append(res)
                    self._escribir_en_log(f"Caso {i}: EXITOSO - {n}")
                else:
                    fallos += 1
                    self._escribir_en_log(f"Caso {i}: RECHAZADO - {log_res}")
            
            except Exception as e:
                fallos += 1
                self._escribir_en_log(f"Caso {i}: ERROR GRAVE CAPTURADO - {e}")
                SistemaLog.registrar(f"Simulación Caso {i} falló: {e}", "CRITICAL")

        self._escribir_en_log(f"\n--- FIN: {exitos} Exitosos, {fallos} Fallos ---")
        messagebox.showinfo("Simulación Finalizada", f"Se procesaron 10 casos.\nExitosos: {exitos}\nFallos: {fallos}")

    def _actualizar_log(self, texto):
        self.txt_output.config(state="normal")
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, texto)
        self.txt_output.config(state="disabled")

    def _escribir_en_log(self, texto):
        """Añade texto al final del log sin borrar lo anterior."""
        self.txt_output.config(state="normal")
        self.txt_output.insert(tk.END, texto + "\n")
        self.txt_output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()