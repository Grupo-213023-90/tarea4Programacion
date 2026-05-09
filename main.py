"""
Módulo: main.py
Descripción: Punto de entrada principal de la aplicación. 
Contiene la interfaz gráfica (GUI) construida con Tkinter y actúa como 
orquestador, uniendo las clases de entidades.py y servicios.py.
Maneja las excepciones para asegurar que el sistema no colapse.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Intentar importar los módulos locales con manejo de errores inmediato
try:
    from entidades import Cliente
    from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
    from logica import Reserva, SistemaLog
    from excepciones import DatosInvalidosError
except ImportError as e:
    print(f"ERROR CRÍTICO: No se encontró un archivo necesario: {e}")
    sys.exit()

class AppSoftwareFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión Integral")
        self.root.geometry("500x650")
        
        # Construir Interfaz
        self._crear_interfaz()
        
        # Registrar inicio en el Log (Fase 4)
        SistemaLog.registrar("Aplicación iniciada correctamente.")

    def _crear_interfaz(self):
        """Define los widgets de la ventana."""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # SECCIÓN CLIENTE
        ttk.Label(main_frame, text="DATOS DEL CLIENTE", font=("Arial", 11, "bold")).pack(pady=5)
        
        ttk.Label(main_frame, text="Nombre Completo:").pack(anchor="w")
        self.ent_nombre = ttk.Entry(main_frame)
        self.ent_nombre.pack(fill="x", pady=2)

        ttk.Label(main_frame, text="Documento:").pack(anchor="w")
        self.ent_doc = ttk.Entry(main_frame)
        self.ent_doc.pack(fill="x", pady=2)

        ttk.Label(main_frame, text="Correo Electrónico:").pack(anchor="w")
        self.ent_correo = ttk.Entry(main_frame)
        self.ent_correo.pack(fill="x", pady=2)

        # SECCIÓN SERVICIO
        ttk.Label(main_frame, text="DETALLES DEL SERVICIO", font=("Arial", 11, "bold")).pack(pady=15)
        
        ttk.Label(main_frame, text="Seleccione Servicio:").pack(anchor="w")
        self.combo_servicio = ttk.Combobox(main_frame, state="readonly", values=[
            "Reserva de Sala", "Alquiler de Equipo", "Asesoría Especializada"
        ])
        self.combo_servicio.pack(fill="x", pady=2)
        self.combo_servicio.current(0)

        ttk.Label(main_frame, text="Valor Unitario ($):").pack(anchor="w")
        self.ent_valor_base = ttk.Entry(main_frame)
        self.ent_valor_base.pack(fill="x", pady=2)

        ttk.Label(main_frame, text="Cantidad:").pack(anchor="w")
        self.ent_cant = ttk.Entry(main_frame)
        self.ent_cant.pack(fill="x", pady=2)

        # BOTÓN
        self.btn_procesar = ttk.Button(main_frame, text="CALCULAR Y REGISTRAR", command=self.procesar_datos)
        self.btn_procesar.pack(pady=20)

        # LOG VISUAL
        self.txt_output = tk.Text(main_frame, height=10, font=("Consolas", 9), state="disabled", bg="#f0f0f0")
        self.txt_output.pack(fill="both", expand=True)

    def procesar_datos(self):
        """Lógica de negocio integrada con manejo de excepciones."""
        try:
            # Captura de datos
            nombre = self.ent_nombre.get()
            doc = self.ent_doc.get()
            correo = self.ent_correo.get()
            v_base = self.ent_valor_base.get()
            cant = self.ent_cant.get()

            # Validar que los campos no estén vacíos antes de instanciar
            if not all([nombre, doc, correo, v_base, cant]):
                raise DatosInvalidosError("Todos los campos son obligatorios.")

            # Instanciar Cliente
            obj_cliente = Cliente(nombre, doc, correo)
            
            # Instanciar Servicio
            tipo = self.combo_servicio.get()
            if tipo == "Reserva de Sala":
                obj_servicio = ReservaSala("S01", int(cant), float(v_base))
            elif tipo == "Alquiler de Equipo":
                obj_servicio = AlquilerEquipo("E01", int(cant), float(v_base))
            else:
                obj_servicio = AsesoriaEspecializada("A01", int(cant), float(v_base))

            # Fase 3: Crear y confirmar Reserva
            mi_reserva = Reserva(obj_cliente, obj_servicio)
            resultado = mi_reserva.confirmar_reserva()

            if mi_reserva.confirmada:
                self._actualizar_log(mi_reserva.generar_comprobante())
                messagebox.showinfo("Software FJ", resultado)
            else:
                messagebox.showwarning("Software FJ", resultado)

        except (ValueError, DatosInvalidosError) as e:
            messagebox.showwarning("Error de Datos", str(e))
            SistemaLog.registrar(f"Error de validación: {e}", "WARNING")
        except Exception as e:
            messagebox.showerror("Error Crítico", f"Fallo inesperado: {e}")
            SistemaLog.registrar(f"Error crítico: {e}", "CRITICAL")

    def _actualizar_log(self, texto):
        """Refresca el área de texto."""
        self.txt_output.config(state="normal")
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, texto)
        self.txt_output.config(state="disabled")

# =========================================================
# ESTA PARTE ES LA QUE HACE QUE LA VENTANA SE MANTENGA ABIERTA
# =========================================================
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AppSoftwareFJ(root)
        root.mainloop() # <--- OBLIGATORIO: Mantiene la app viva
    except Exception as e:
        print(f"No se pudo iniciar la interfaz: {e}")