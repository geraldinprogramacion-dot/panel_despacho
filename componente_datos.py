from abc import ABC, abstractmethod

class Vehiculo(ABC):
    def __init__(self, id_vehiculo, modelo, kilometraje, lat, lng):
        self.id = id_vehiculo
        self.modelo = modelo
        self.kilometraje = kilometraje
        self.lat = lat
        self.lng = lng

    @abstractmethod
    def requiere_mantenimiento(self):
        pass

class Auto(Vehiculo):
    def requiere_mantenimiento(self):
        # Un auto requiere mantenimiento si supera los 10,000 km
        return self.kilometraje > 10000

class Camion(Vehiculo):
    def requiere_mantenimiento(self):
        # Un camión requiere mantenimiento si supera los 20,000 km
        return self.kilometraje > 20000

class Furgoneta(Vehiculo):
    def requiere_mantenimiento(self):
        # Una furgoneta requiere mantenimiento si supera los 15,000 km
        return self.kilometraje > 15000

def obtener_vehiculos():
    return [
        Auto("V-01", "Toyota Hilux", 12000, 42.8467, -2.6716),
        Camion("V-02", "Renault Kangoo", 18500, 42.8520, -2.6800),
        Furgoneta("V-03", "Ford Transit", 9500, 42.8400, -2.6650)
    ]
