"""
Módulo: excepciones.py
Autor: Diyein Erlency Botero Betancourt
Descripción: Definición de excepciones personalizadas para Software FJ.
Principio POO: Herencia (Heredamos de la clase Base Exception).
"""

class SoftwareFJError(Exception):
    """Clase base para errores del sistema."""
    pass

class DatosInvalidosError(SoftwareFJError):
    """Error cuando los datos del formulario son incorrectos."""
    def __init__(self, mensaje="Datos de entrada no válidos."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ServicioNoDisponibleError(SoftwareFJError):
    """Error cuando el servicio solicitado no puede procesarse."""
    def __init__(self, servicio):
        self.mensaje = f"El servicio '{servicio}' no está disponible por el momento."
        super().__init__(self.mensaje)