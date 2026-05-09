"""
Módulo: logica.py
Autor: Juan Esteban Cardenas Alvarez
Descripción: Implementa la clase Reserva para vincular Clientes con Servicios.
Principios POO: Composición y Manejo Avanzado de Excepciones.
"""

import datetime
from excepciones import DatosInvalidosError, ServicioNoDisponibleError

class SistemaLog:
    """Gestiona el registro de eventos en un archivo de texto."""
    ARCHIVO = "log_sistema.txt"

    @staticmethod
    def registrar(evento, nivel="INFO"):
        """Escribe en el archivo txt con fecha y hora actual."""
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(SistemaLog.ARCHIVO, "a", encoding="utf-8") as f:
                f.write(f"[{fecha}] [{nivel}] {evento}\n")
        except Exception as e:
            print(f"Error escribiendo log: {e}")

class Reserva:
    """Relaciona Cliente con Servicio aplicando manejo de excepciones."""
    def __init__(self, cliente, servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.confirmada = False

    def confirmar_reserva(self):
        """
        Aplica try/except/else/finally para validar la reserva.
        Registra cada paso en el Log.
        """
        try:
            SistemaLog.registrar(f"Validando reserva para: {self.cliente.nombre}")
            
            # Validación de ejemplo
            if self.servicio.costo_base <= 0:
                raise DatosInvalidosError("El costo base debe ser mayor a cero.")
            
            costo = self.servicio.calcular_costo()
            
        except (DatosInvalidosError, ServicioNoDisponibleError) as e:
            SistemaLog.registrar(f"Error controlado: {e}", "ADVERTENCIA")
            self.confirmada = False
            return str(e)
        except Exception as e:
            SistemaLog.registrar(f"Error crítico: {e}", "ERROR")
            self.confirmada = False
            return "Error interno del servidor."
        else:
            # Solo si todo salió bien
            self.confirmada = True
            msg = f"Reserva confirmada por ${costo:,.0f}"
            SistemaLog.registrar(msg, "EXITO")
            return msg
        finally:
            SistemaLog.registrar("Finalizó intento de confirmación.")

    def generar_comprobante(self):
        """Retorna el texto final con el correo incluido."""
        return (
            f"--- COMPROBANTE FJ ---\n"
            f"{self.cliente.mostrar_detalles()}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Total: ${self.servicio.calcular_costo():,.0f}\n"
            f"-----------------------"
        )