"""
Módulo: servicios.py
Autor 1: Juan Esteban Cardenas Alvarez
Autor 2: Diyein Erlency Botero Betancourt
Descripción: Este módulo contiene la Fase 2 (Catálogo de Servicios). 
Implementa la Herencia y el Polimorfismo. Define los diferentes servicios 
que ofrece la empresa y cómo se calcula el costo de cada uno.
"""

from abc import ABC, abstractmethod
from entidades import EntidadGeneral

class Servicio(EntidadGeneral, ABC):
    """
    Clase abstracta intermedia para servicios. 
    Hereda de EntidadGeneral para mantener la coherencia del sistema.
    """
    def __init__(self, id_servicio, nombre, costo_base):
        self.id_servicio = id_servicio
        self.nombre = nombre
        # El costo base es dinámico y lo ingresa el usuario
        self.costo_base = float(costo_base)

    @abstractmethod
    def calcular_costo(self):
        """Método polimórfico para calcular el precio final según el servicio."""
        pass
    
    def mostrar_detalles(self):
        """Retorna la descripción básica del servicio."""
        return f"ID: {self.id_servicio} | Servicio: {self.nombre}"

class ReservaSala(Servicio):
    """Implementa el servicio de reserva de salas por horas."""
    def __init__(self, id_servicio, cantidad, costo_base):
        super().__init__(id_servicio, "Reserva de Sala", costo_base)
        self.horas = cantidad

    def calcular_costo(self):
        """Cálculo simple: Costo base por cantidad de horas."""
        return self.costo_base * self.horas

class AlquilerEquipo(Servicio):
    """Implementa el servicio de alquiler de hardware por días."""
    def __init__(self, id_servicio, cantidad, costo_base):
        super().__init__(id_servicio, "Alquiler de Equipo", costo_base)
        self.dias = cantidad

    def calcular_costo(self):
        """
        Polimorfismo: Aplica un descuento del 10% si el alquiler es
        mayor a 5 días.
        """
        total = self.costo_base * self.dias
        return total * 0.9 if self.dias > 5 else total

class AsesoriaEspecializada(Servicio):
    """Implementa consultorías profesionales cobradas por horas."""
    def __init__(self, id_servicio, cantidad, costo_base):
        super().__init__(id_servicio, "Asesoría Especializada", costo_base)
        self.horas = cantidad

    def calcular_costo(self):
        """
        Polimorfismo: Aplica un recargo del 15% por concepto de
        especialidad técnica.
        """
        return (self.costo_base * self.horas) * 1.15