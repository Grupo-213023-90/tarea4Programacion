"""
Módulo: entidades.py
Autor: Fredy Andrés Tangarife Correa
Descripción: Este módulo contiene la Fase 1 (Cimientos y Datos). 
Define la abstracción principal del sistema y la gestión de clientes, 
aplicando los principios de Abstracción y Encapsulamiento.
"""

from abc import ABC, abstractmethod
import re

class EntidadGeneral(ABC):
    """
    Clase abstracta de máximo nivel. 
    Define que todos los componentes del sistema deben poder mostrar su información.
    """
    @abstractmethod
    def mostrar_detalles(self):
        """Método obligatorio para ser sobrescrito en clases derivadas."""
        pass

class Cliente(EntidadGeneral):
    """
    Clase que gestiona la información de los clientes de Software FJ.
    Aplica encapsulación mediante atributos privados y decoradores.
    """
    def __init__(self, nombre, documento, correo):
        # Atributos privados (__), inaccesibles directamente desde fuera de la clase
        self.__nombre = self.__validar_nombre(nombre)
        self.__documento = self.__validar_documento(documento)
        self.__correo = self.__validar_correo(correo)

    def __validar_nombre(self, nombre):
        """Asegura que el nombre tenga una longitud mínima aceptable."""
        if len(nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip()

    def __validar_documento(self, documento):
        """Valida que el documento de identidad contenga solo números."""
        if not documento.isdigit():
            raise ValueError("El documento debe contener únicamente números.")
        return documento

    def __validar_correo(self, correo):
        """Valida el formato de correo electrónico mediante expresiones regulares."""
        patron = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(patron, correo):
            raise ValueError("El formato del correo electrónico es inválido.")
        return correo

    @property
    def nombre(self):
        """Permite leer el nombre del cliente de forma controlada."""
        return self.__nombre

    @property
    def correo(self):
        """Permite leer el correo del cliente de forma controlada."""
        return self.__correo

    def mostrar_detalles(self):
        """Implementación del contrato de EntidadGeneral para el cliente."""
        return f"Cliente: {self.__nombre} | Doc: {self.__documento} | Email: {self.__correo}"