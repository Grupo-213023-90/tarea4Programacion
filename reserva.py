"""
Software FJ - Versión Integrada

Autores:
- Fredy Andrés Tangarife Correa (Base del sistema)
- Juan Esteban Cárdenas Álvarez (Gestión de Reservas)
"""

import tkinter as tk
from tkinter import messagebox, ttk
import re
import logging
from abc import ABC, abstractmethod

# =========================================================
# 1. CONFIGURACIÓN DE LOGS
# =========================================================
logging.basicConfig(
    filename='sistema_software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =========================================================
# 2. EXCEPCIONES
# =========================================================
class DatoInvalidoError(Exception):
    pass

class DatosInvalidosError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass

class OperacionNoPermitidaError(Exception):
    pass

# =========================================================
# 3. BASE DEL SISTEMA (FREDY)
# =========================================================
class EntidadGeneral(ABC):
    @abstractmethod
    def mostrar_detalles(self):
        pass


class Cliente(EntidadGeneral):
    def __init__(self, nombre, documento, correo):
        self.__nombre = None
        self.__documento = None
        self.__correo = None

        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]{3,50}$", valor):
            raise DatoInvalidoError("Nombre inválido")
        self.__nombre = valor

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not re.match(r"^\d{7,12}$", valor):
            raise DatoInvalidoError("Documento inválido")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', valor):
            raise DatoInvalidoError("Correo inválido")
        self.__correo = valor

    def mostrar_detalles(self):
        return f"{self.__nombre} | {self.__documento} | {self.__correo}"

# =========================================================
# 4. APORTE JUAN ESTEBAN - RESERVAS
# =========================================================
class Servicio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        pass


class ReservaSala(Servicio):
    def calcular_costo(self, duracion, **kwargs):
        return self.costo_base * duracion


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion, **kwargs):
        return (self.costo_base * duracion) * 0.9


class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, **kwargs):
        return self.costo_base * duracion * 1.2


class Reserva:
    def __init__(self, cliente, servicio, duracion, **kwargs):

        if cliente is None:
            raise DatosInvalidosError("Cliente nulo")

        if servicio is None:
            raise ServicioNoDisponibleError("Servicio inválido")

        if duracion <= 0:
            raise DatosInvalidosError("Duración inválida")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.costo_total = 0

    def confirmar(self):
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError("No disponible")

            self.costo_total = self.servicio.calcular_costo(self.duracion)

            if self.costo_total <= 0:
                raise ValueError("Costo inválido")

        except Exception as e:
            self.estado = "ERROR"
            raise e

        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("Ya cancelada")

        self.estado = "CANCELADA"
        self.servicio.disponible = True

# =========================================================
# 5. INTERFAZ GRÁFICA (ARREGLADA)
# =========================================================
class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ")
        self.root.geometry("600x450")

        self.lista_clientes = []

        frame = ttk.LabelFrame(root, text="Registro Cliente", padding=10)
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Nombre").grid(row=0, column=0, pady=5)
        self.nombre = ttk.Entry(frame, width=30)
        self.nombre.grid(row=0, column=1)

        ttk.Label(frame, text="Documento").grid(row=1, column=0, pady=5)
        self.doc = ttk.Entry(frame, width=30)
        self.doc.grid(row=1, column=1)

        ttk.Label(frame, text="Correo").grid(row=2, column=0, pady=5)
        self.correo = ttk.Entry(frame, width=30)
        self.correo.grid(row=2, column=1)

        ttk.Button(frame, text="Registrar", command=self.registrar).grid(row=3, columnspan=2, pady=10)

        # Área de visualización
        self.texto = tk.Text(root, height=10)
        self.texto.pack(padx=20, pady=10)

    def registrar(self):
        try:
            c = Cliente(self.nombre.get(), self.doc.get(), self.correo.get())
            self.lista_clientes.append(c)

            self.texto.insert(tk.END, c.mostrar_detalles() + "\n")

            messagebox.showinfo("OK", "Cliente registrado")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# =========================================================
# 6. EJECUCIÓN
# =========================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()