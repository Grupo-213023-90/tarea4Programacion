"""
Fase: Cimientos y Datos - Software FJ
Estudiante: Fredy Andrés Tangarife Correa
Descripción: Implementación de arquitectura POO base, validaciones 
estrictas, interfaz gráfica y sistema de trazabilidad por logs.
"""
#Librería encargada de la interfaz gráfica de usuario (GUI)
# y la programación orientada a objetos.
import tkinter as tk
from tkinter import messagebox, ttk
import re
import logging
from abc import ABC, abstractmethod

# =========================================================
# 1. CONFIGURACIÓN DE LOGS (Registro de eventos y errores)
# =========================================================
logging.basicConfig(
    filename='sistema_software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =========================================================
# 2. EXCEPCIÓN PERSONALIZADA
# =========================================================
class DatoInvalidoError(Exception):
    """Excepción lanzada cuando un dato no cumple con las validaciones estrictas."""
    pass

# =========================================================
# 3. LÓGICA DE NEGOCIO (CAPA DE DATOS)
# =========================================================

class EntidadGeneral(ABC):
    """Clase abstracta que representa una entidad base en el sistema."""
    
    @abstractmethod
    def mostrar_detalles(self):
        """Método obligatorio para mostrar la información de la entidad."""
        pass

class Cliente(EntidadGeneral):
    """
    Representa a un cliente del sistema Software FJ.
    Implementa encapsulación, validaciones y propiedades.
    """
    def __init__(self, nombre, documento, correo):
        # Atributos privados
        self.__nombre = None
        self.__documento = None
        self.__correo = None
        
        # Uso de setters para validar desde la creación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        logging.info(f"Instancia de Cliente creada: {self.nombre}")

    # --- Propiedades con decoradores @property ---

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida que el nombre solo contenga letras y espacios."""
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]{3,50}$", valor):
            raise DatoInvalidoError("El nombre debe tener solo letras (mín. 3).")
        self.__nombre = valor

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        """Valida que el documento sea numérico de 7 a 12 dígitos."""
        if not re.match(r"^\d{7,12}$", valor):
            raise DatoInvalidoError("El documento debe ser numérico (7-12 dígitos).")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        """Valida el formato de correo electrónico."""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, valor):
            raise DatoInvalidoError("El formato de correo es inválido.")
        self.__correo = valor

    def mostrar_detalles(self):
        """Devuelve una cadena con los datos del cliente."""
        return f"NOMBRE: {self.__nombre} | DOC: {self.__documento} | EMAIL: {self.__correo}"

# =========================================================
# 4. INTERFAZ GRÁFICA (TKINTER)
# =========================================================

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión de Clientes (Fase Cimientos)")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")

        # Lista interna para simular "base de datos" en memoria
        self.lista_clientes = []

        # --- Estilos ---
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))

        # --- Widgets de Entrada ---
        frame_entrada = ttk.LabelFrame(self.root, text=" Registro de Nuevo Cliente ", padding=10)
        frame_entrada.pack(pady=20, padx=20, fill="x")

        ttk.Label(frame_entrada, text="Nombre Completo:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_nombre = ttk.Entry(frame_entrada, width=40)
        self.ent_nombre.grid(row=0, column=1, pady=5)

<<<<<<< HEAD
# ==========================================
# 5. GESTIÓN DE RESERVAS
# ==========================================
class Reserva:
    """
    Clase que gestiona la relación entre Cliente y Servicio.
    Implementa confirmación, cancelación y manejo avanzado de excepciones.
    """

    def __init__(self, cliente, servicio, duracion, **kwargs):
        # Validaciones más robustas
        if cliente is None or not hasattr(cliente, "nombre"):
            raise DatosInvalidosError("Cliente inválido.")

        if servicio is None or not hasattr(servicio, "calcular_costo"):
            raise ServicioNoDisponibleError("Servicio inválido.")

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor a 0.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.parametros_extra = kwargs
        self.costo_total = 0

    def confirmar(self):
        logging.info(f"Iniciando reserva para {self.cliente.nombre}")

        try:
            # Validar disponibilidad
            if not getattr(self.servicio, "disponible", False):
                raise ServicioNoDisponibleError(
                    f"Servicio '{self.servicio.nombre}' no disponible"
                )

            # Calcular costo (polimorfismo)
            self.costo_total = self.servicio.calcular_costo(
                self.duracion, **self.parametros_extra
            )

            # Validar costo
            if self.costo_total <= 0:
                raise ValueError("Costo inválido")

        except ServicioNoDisponibleError as e:
            self.estado = "RECHAZADA"
            logging.error(e)
            raise

        except ValueError as e:
            self.estado = "ERROR_CALCULO"
            logging.error(e)
            raise DatosInvalidosError("Error en cálculo") from e

        except Exception as e:
            self.estado = "ERROR_CRITICO"
            logging.critical(e)
            raise

        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False
            logging.info(f"Reserva confirmada: ${self.costo_total}")

        finally:
            logging.info(f"Estado final: {self.estado}")

    def cancelar(self):
        if self.estado in ["CANCELADA", "RECHAZADA"]:
            raise OperacionNoPermitidaError("No se puede cancelar este estado.")

        self.estado = "CANCELADA"
        self.servicio.disponible = True
        logging.info(f"Reserva cancelada: {self.cliente.nombre}")

    def mostrar_resumen(self):
        return (
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo_total}"
        )
# ==========================================
# 6. SIMULACIÓN DEL SISTEMA (10 OPERACIONES)
# ==========================================
def main():
    print("Iniciando Sistema Software FJ...\nVerifique el archivo 'software_fj_logs.txt' para ver los registros.")
    logging.info("--- NUEVA SESIÓN INICIADA ---")

    # Listas internas (sin bases de datos)
    clientes = []
    servicios = []
    reservas = []

    print("\n--- SIMULANDO OPERACIONES ---")

    # 1. Registro exitoso de cliente
    try:
        c1 = Cliente("1001", "Fredy Tangarife", "fredy@unad.edu.co")
        clientes.append(c1)
        logging.info(f"Cliente registrado: {c1.nombre}")
    except Exception as e: print(e)

    # 2. Registro fallido de cliente (Correo inválido)
    try:
        c_error = Cliente("1002", "Luis Gomez", "luis.sin.arroba.com")
    except Exception as e:
        logging.error(f"Fallo al registrar cliente 2: {e}")

    # 3. Registro fallido de cliente (Nombre vacío)
    try:
        c_error2 = Cliente("1003", "", "juan@correo.com")
    except Exception as e:
        logging.error(f"Fallo al registrar cliente 3: {e}")

    # 4. Creación de Servicios exitosa (Polimorfismo)
    sala1 = ReservaSala("S01", "Sala Juntas A", 20000, 10)
    equipo1 = AlquilerEquipo("E01", "Proyector 4K", 50000)
    asesoria1 = AsesoriaEspecializada("A01", "Arquitectura de Software", 100000, "Jose Castro")
    servicios.extend([sala1, equipo1, asesoria1])

    # 5. Creación fallida de Servicio (Costo negativo)
    try:
        sala_error = ReservaSala("S02", "Sala VIP", -100, 5)
    except Exception as e:
        logging.error(f"Fallo al crear servicio: {e}")

    # 6. Reserva exitosa (Uso de sobrecarga con incluye_catering=True)
    try:
        reserva1 = Reserva(c1, sala1, 4, incluye_catering=True)
        reserva1.confirmar()
        reservas.append(reserva1)
    except Exception as e: print(e)

    # 7. Intento de reserva de servicio ya ocupado
    try:
        c2 = Cliente("1004", "Diyein Botero", "diyein@correo.com")
        clientes.append(c2)
        reserva_fallida = Reserva(c2, sala1, 2) # sala1 ya no está disponible
        reserva_fallida.confirmar()
    except Exception as e:
        print(f"Controlado en main - No se pudo reservar: {e}")

    # 8. Reserva exitosa con cálculo sobrecargado (descuento)
    try:
        reserva2 = Reserva(c2, equipo1, 5, aplicar_descuento=True)
        reserva2.confirmar()
        reservas.append(reserva2)
    except Exception as e: print(e)

    # 9. Cancelación de reserva exitosa
    try:
        reserva1.cancelar()
    except Exception as e: print(e)

    # 10. Operación no permitida (Cancelar algo ya cancelado)
    try:
        reserva1.cancelar()
    except Exception as e:
        logging.warning(f"Intento de doble cancelación detectado: {e}")
        print(f"Controlado en main - Error: {e}")

    print("\nSimulación finalizada. Revisa el archivo 'software_fj_logs.txt'.")

=======
        ttk.Label(frame_entrada, text="Documento:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_documento = ttk.Entry(frame_entrada, width=40)
        self.ent_documento.grid(row=1, column=1, pady=5)

        ttk.Label(frame_entrada, text="Correo Electrónico:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_correo = ttk.Entry(frame_entrada, width=40)
        self.ent_correo.grid(row=2, column=1, pady=5)

        # Botón de Registro
        self.btn_registrar = ttk.Button(frame_entrada, text="Registrar Cliente", command=self.registrar_cliente)
        self.btn_registrar.grid(row=3, column=0, columnspan=2, pady=15)

        # --- Visualización de Datos ---
        ttk.Label(self.root, text="Clientes Registrados:").pack(anchor="w", padx=25)
        self.txt_visualizacion = tk.Text(self.root, height=10, width=70, state="disabled", font=("Courier", 9))
        self.txt_visualizacion.pack(pady=10, padx=20)

    def registrar_cliente(self):
        """Captura los datos, crea el objeto y maneja excepciones."""
        nombre = self.ent_nombre.get()
        doc = self.ent_documento.get()
        correo = self.ent_correo.get()

        try:
            # Intentar crear el objeto (aquí se disparan los @property setters)
            nuevo_cliente = Cliente(nombre, doc, correo)
            
            # Si tiene éxito, agregar a la lista
            self.lista_clientes.append(nuevo_cliente)
            self.actualizar_pantalla(f"[ÉXITO] {nuevo_cliente.mostrar_detalles()}")
            
            # Limpiar campos
            self.limpiar_campos()
            messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente.")

        except DatoInvalidoError as e:
            # Error de validación de datos (Controlado)
            messagebox.showwarning("Dato Inválido", str(e))
            logging.warning(f"Error de validación en GUI: {e}")

        except Exception as e:
            # Error inesperado (Encadenamiento y Log)
            messagebox.showerror("Error Crítico", "Ocurrió un error inesperado en el sistema.")
            logging.critical(f"Error no controlado: {e}", exc_info=True)
        
        finally:
            print("Intento de registro procesado.")

    def actualizar_pantalla(self, mensaje):
        """Actualiza el área de texto con la información más reciente."""
        self.txt_visualizacion.config(state="normal")
        self.txt_visualizacion.insert(tk.END, mensaje + "\n")
        self.txt_visualizacion.config(state="disabled")

    def limpiar_campos(self):
        """Limpia los campos de entrada."""
        self.ent_nombre.delete(0, tk.END)
        self.ent_documento.delete(0, tk.END)
        self.ent_correo.delete(0, tk.END)

# =========================================================
# 5. EJECUCIÓN DEL PROGRAMA
# =========================================================
>>>>>>> 303082e26a64962f13d161b9a6c3fe9fb8f09bf8
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()