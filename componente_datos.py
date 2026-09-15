from abc import ABC, abstractmethod

# 1. Clase abstracta base (plantilla general)
class Vehiculo(ABC):
    def __init__(self, placa, modelo, estado, lat, lon):
        self.placa = placa
        self.modelo = modelo
        self.estado = estado  # "Operativo" o "En Mantenimiento"
        self.lat = lat
        self.lon = lon

    @abstractmethod
    def detalles_especificos(self):
        pass

# 2. Subclase Auto (Hereda de Vehiculo)
class Auto(Vehiculo):
    def detalles_especificos(self):
        return f"Auto Turístico - Modelo: {self.modelo}"

# 3. Subclase Camion (Hereda de Vehiculo)
class Camion(Vehiculo):
    def detalles_especificos(self):
        return f"Camión de Carga Pesada - Modelo: {self.modelo}"

# 4. Subclase Furgoneta (Hereda de Vehiculo)
class Furgoneta(Vehiculo):
    def detalles_especificos(self):
        return f"Furgoneta de Reparto - Modelo: {self.modelo}"

# 5. Función que devuelve la lista de objetos creados
def obtener_vehiculos():
    return [
        Auto("ABC-1234", "Toyota Corolla", "Operativo", 42.8467, -2.6716),
        Camion("XYZ-9876", "Volvo FH", "En Mantenimiento", 42.8550, -2.6500),
        Furgoneta("DEF-5678", "Mercedes Sprinter", "Operativo", 42.8400, -2.6800)
    ]
