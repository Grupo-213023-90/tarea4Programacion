"""
Módulo: main.py
Descripción: Punto de entrada principal de la aplicación. 
Contiene la interfaz gráfica (GUI) construida con Tkinter y actúa como 
orquestador, uniendo las clases de entidades.py y servicios.py.
Maneja las excepciones para asegurar que el sistema no colapse.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Importamos las clases definidas en los módulos anteriores
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

class AppSoftwareFJ:
    """Clase principal de la aplicación GUI."""
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión de Servicios")
        self.root.geometry("500x650")
        
        # Llamada a la construcción de los elementos visuales
        self._crear_interfaz()

    def _crear_interfaz(self):
        """Dibuja todos los widgets necesarios en la ventana."""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # SECCIÓN DE DATOS PERSONALES
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

        # SECCIÓN DE SERVICIOS
        ttk.Label(main_frame, text="DETALLES DEL SERVICIO", font=("Arial", 11, "bold")).pack(pady=15)
        
        ttk.Label(main_frame, text="Seleccione Servicio:").pack(anchor="w")
        self.combo_servicio = ttk.Combobox(main_frame, state="readonly", values=[
            "Reserva de Sala", "Alquiler de Equipo", "Asesoría Especializada"
        ])
        self.combo_servicio.pack(fill="x", pady=2)
        self.combo_servicio.current(0)

        # Entrada para valor digitado por el usuario
        ttk.Label(main_frame, text="Valor de la Hora/Día ($):").pack(anchor="w")
        self.ent_valor_base = ttk.Entry(main_frame)
        self.ent_valor_base.pack(fill="x", pady=2)

        ttk.Label(main_frame, text="Cantidad (Horas o Días):").pack(anchor="w")
        self.ent_cant = ttk.Entry(main_frame)
        self.ent_cant.pack(fill="x", pady=2)

        # Botón procesador
        self.btn_procesar = ttk.Button(main_frame, text="CALCULAR Y REGISTRAR", command=self.procesar_datos)
        self.btn_procesar.pack(pady=20)

        # Área de log de resultados
        self.txt_output = tk.Text(main_frame, height=10, font=("Consolas", 9), state="disabled", bg="#f0f0f0")
        self.txt_output.pack(fill="both", expand=True)

    def procesar_datos(self):
        """
        Captura datos, maneja excepciones e integra los módulos.
        Garantiza que el sistema no se detenga por errores de usuario.
        """
        try:
            # Validación de entradas numéricas iniciales
            raw_cant = self.ent_cant.get()
            raw_valor = self.ent_valor_base.get()

            if not raw_cant.isdigit() or not raw_valor.replace('.', '', 1).isdigit():
                raise ValueError("La cantidad y el valor base deben ser números válidos.")
            
            cant = int(raw_cant)
            valor_base = float(raw_valor)

            # Instanciación del Cliente (Activa validaciones de entidades.py)
            cli = Cliente(self.ent_nombre.get(), self.ent_doc.get(), self.ent_correo.get())
            
            # Instanciación polimórfica del Servicio (Fase 2)
            tipo = self.combo_servicio.get()
            
            if tipo == "Reserva de Sala":
                srv = ReservaSala("SRV-001", cant, valor_base)
            elif tipo == "Alquiler de Equipo":
                srv = AlquilerEquipo("SRV-002", cant, valor_base)
            else:
                srv = AsesoriaEspecializada("SRV-003", cant, valor_base)

            # Ejecución de la lógica de negocio
            costo_final = srv.calcular_costo()
            
            # Formateo del resumen para el usuario
            resumen = (
                f"--- OPERACIÓN EXITOSA ---\n"
                f"{cli.mostrar_detalles()}\n"  # Muestra nombre, documento y correo
                f"Servicio: {srv.nombre}\n"
                f"Valor Unitario: ${valor_base:,.0f}\n"
                f"Costo Final: ${costo_final:,.0f}\n"
                f"--------------------------"
            )
            self._actualizar_log(resumen)

        except ValueError as e:
            # Captura errores de validación de las clases
            messagebox.showwarning("Dato Inválido", f"Atención: {e}")
        except Exception as e:
            # Captura errores críticos inesperados
            messagebox.showerror("Fallo de Sistema", f"Ocurrió un error inesperado: {e}")

    def _actualizar_log(self, texto):
        """Método auxiliar para refrescar el cuadro de texto de salida."""
        self.txt_output.config(state="normal")
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, texto)
        self.txt_output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()