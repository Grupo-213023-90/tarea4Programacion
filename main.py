"""
Proyecto: Sistema Integral de Gestión - Software FJ
Institución: Universidad Nacional Abierta y a Distancia (UNAD)
Equipo de Desarrollo:
- LUIS DAVID GOMEZ PINTO
- JOSE GABRIEL CASTRO LOPEZ
- JUAN ESTEBAN CARDENAS ALVAREZ
- DIYEIN ERLENCY BOTERO BETANCOURT
- FREDY ANDRES TANGARIFE CORREA
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE LOGS
# ==========================================
logging.basicConfig(
    filename='software_fj_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================
class SistemaFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class DatosInvalidosError(SistemaFJError):
    """Excepción para datos faltantes o incorrectos."""
    pass

class ServicioNoDisponibleError(SistemaFJError):
    """Excepción para cuando un servicio no se puede reservar."""
    pass

class OperacionNoPermitidaError(SistemaFJError):
    """Excepción para transacciones de estado inválidas."""
    pass

# ==========================================
# 3. CLASES ABSTRACTAS Y ENTIDADES BASE
# ==========================================
class EntidadGeneral(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    @abstractmethod
    def mostrar_detalles(self):
        pass

class Cliente(EntidadGeneral):
    """Clase con encapsulamiento estricto."""
    def __init__(self, documento, nombre, correo):
        self.__documento = self._validar_texto(documento, "Documento")
        self.__nombre = self._validar_texto(nombre, "Nombre")
        self.__correo = self._validar_correo(correo)

    def _validar_texto(self, valor, campo):
        if not valor or not isinstance(valor, str) or valor.strip() == "":
            raise DatosInvalidosError(f"El campo '{campo}' no puede estar vacío.")
        return valor.strip()

    def _validar_correo(self, correo):
        if "@" not in str(correo) or "." not in str(correo):
            raise DatosInvalidosError("Formato de correo inválido.")
        return correo.strip()
    
    # Getters
    @property
    def nombre(self): return self.__nombre
    @property
    def documento(self): return self.__documento
    
    def mostrar_detalles(self):
        return f"Cliente: {self.__nombre} (Doc: {self.__documento})"

class Servicio(EntidadGeneral):
    """Clase abstracta para los servicios."""
    def __init__(self, id_servicio, nombre, costo_base):
        if costo_base < 0:
            raise DatosInvalidosError("El costo base no puede ser negativo.")
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Método que será sobreescrito (polimorfismo) y 'sobrecargado' en las hijas."""
        pass

# ==========================================
# 4. CLASES DERIVADAS (SERVICIOS) - Polimorfismo
# ==========================================
class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, capacidad):
        super().__init__(id_servicio, nombre, costo_base)
        self.capacidad = capacidad

    # Simulación de sobrecarga mediante parámetros opcionales
    def calcular_costo(self, horas, incluye_catering=False):
        costo = self.costo_base * horas
        if incluye_catering:
            costo += 50000  # Costo fijo extra
        return costo

    def mostrar_detalles(self):
        return f"Sala '{self.nombre}' (Cap: {self.capacidad} pers.)"

class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, requiere_deposito=True):
        super().__init__(id_servicio, nombre, costo_base)
        self.requiere_deposito = requiere_deposito

    # Sobrecarga: cálculo diferente al de la sala
    def calcular_costo(self, dias, aplicar_descuento=False):
        costo = self.costo_base * dias
        if aplicar_descuento and dias > 3:
            costo *= 0.90  # 10% de descuento
        return costo

    def mostrar_detalles(self):
        return f"Equipo '{self.nombre}' (Depósito: {'Sí' if self.requiere_deposito else 'No'})"

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, especialista):
        super().__init__(id_servicio, nombre, costo_base)
        self.especialista = especialista

    def calcular_costo(self, horas, nivel_urgencia="normal"):
        recargo = 1.5 if nivel_urgencia == "alta" else 1.0
        return (self.costo_base * horas) * recargo

    def mostrar_detalles(self):
        return f"Asesoría en '{self.nombre}' con {self.especialista}"

# ==========================================
# 5. GESTIÓN DE RESERVAS
# ==========================================
class Reserva:
    def __init__(self, cliente, servicio, duracion, **kwargs):
        # Validaciones iniciales (mejora importante)
        if cliente is None:
            raise DatosInvalidosError("El cliente no puede ser nulo.")
        if servicio is None:
            raise ServicioNoDisponibleError("Debe especificar un servicio válido.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser un número mayor a 0.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.parametros_extra = kwargs
        self.costo_total = 0

    def confirmar(self):
        logging.info(f"Iniciando confirmación de reserva para {self.cliente.nombre}.")

        try:
            # Validar disponibilidad
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' no está disponible."
                )

            # Polimorfismo (cada servicio calcula distinto)
            self.costo_total = self.servicio.calcular_costo(
                self.duracion, **self.parametros_extra
            )

            # Validación de coherencia del costo
            if self.costo_total <= 0:
                raise ValueError("El costo calculado es inválido.")

        except ServicioNoDisponibleError as e:
            logging.error(f"Error de disponibilidad: {e}")
            self.estado = "RECHAZADA"
            raise  # Mantiene la lógica del main

        except ValueError as e:
            logging.error(f"Error en cálculo: {e}")
            self.estado = "ERROR_CALCULO"
            raise DatosInvalidosError(
                "Fallo interno al calcular el costo del servicio"
            ) from e

        except Exception as e:
            logging.critical(f"Error inesperado: {e}")
            self.estado = "ERROR_CRITICO"
            raise

        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False
            logging.info(f"Reserva confirmada. Total: ${self.costo_total}")

        finally:
            logging.info(f"Proceso finalizado. Estado: {self.estado}")

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya fue cancelada.")

        self.estado = "CANCELADA"
        self.servicio.disponible = True
        logging.info(f"Reserva cancelada para {self.cliente.nombre}.")


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

if __name__ == "__main__":
    main()