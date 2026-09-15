from abc import ABC, abstractmethod
import pandas as pd


# 1. Clase madre (abstracta)
class Vehiculo(ABC):

    def __init__(
        self,
        id_v: str,
        matricula: str,
        modelo: str,
        kilometraje: int,
        lat: float,
        lng: float,
    ):
        self.id = id_v
        self.matricula = matricula
        self.modelo = modelo
        self.kilometraje = int(kilometraje)
        self.lat = float(lat)
        self.lng = float(lng)

    @abstractmethod
    def requiere_mantenimiento(self) -> bool:
        """Método polimórfico a implementar por cada clase hija."""
        pass


# 2. Clases hijas (Subclases)
class Furgoneta(Vehiculo):

    def requiere_mantenimiento(self) -> bool:
        return self.kilometraje >= 15000


class VehiculoElectrico(Vehiculo):

    def requiere_mantenimiento(self) -> bool:
        return self.kilometraje >= 5000


# 3. Integración en el Ingestor/Factoría
class IngestorDatos:
    """Componente independiente para la ingesta, limpieza y validación de datos de la flota."""

    def __init__(self):
        pass

    def crear_vehiculo(self, datos: dict) -> Vehiculo:
        """Fabrica el objeto correspondiente según el tipo."""
        tipo = datos.get("tipo")
        params = {
            "id_v": datos["id"],
            "matricula": datos["matricula"],
            "modelo": datos["modelo"],
            "kilometraje": datos["kilometraje"],
            "lat": datos["lat"],
            "lng": datos["lng"],
        }

        if tipo == "Furgoneta":
            return Furgoneta(**params)
        elif tipo == "Electrico":
            return VehiculoElectrico(**params)
        else:
            raise ValueError(f"Tipo de vehículo no soportado: {tipo}")

    def cargar_datos_flota(self) -> pd.DataFrame:
        try:
            datos_raw = [
                {
                    "id": "V-001",
                    "matricula": "4821-KBC",
                    "modelo": "Mercedes Vito Tourer 2016",
                    "tipo": "Furgoneta",
                    "kilometraje": 16200,
                    "lat": 42.8467,
                    "lng": -2.6716,
                },
                {
                    "id": "V-002",
                    "matricula": "9102-LMN",
                    "modelo": "Renault Master 2021",
                    "tipo": "Furgoneta",
                    "kilometraje": 11400,
                    "lat": 42.8520,
                    "lng": -2.6810,
                },
                {
                    "id": "E-001",
                    "matricula": "3341-NXZ",
                    "modelo": "Nissan Townstar EV 2023",
                    "tipo": "Electrico",
                    "kilometraje": 5300,
                    "lat": 42.8412,
                    "lng": -2.6650,
                },
            ]

            df = pd.DataFrame(datos_raw)

            # Validar contrato
            columnas_requeridas = {
                "id",
                "matricula",
                "modelo",
                "tipo",
                "kilometraje",
                "lat",
                "lng",
            }
            if not columnas_requeridas.issubset(df.columns):
                raise ValueError(
                    f"El conjunto de datos no cumple el contrato. Columnas requeridas: {columnas_requeridas}"
                )

            # Instanciación de objetos e invocación polimórfica
            objetos_vehiculo = [
                self.crear_vehiculo(row) for row in datos_raw
            ]

            df["requiere_mantenimiento"] = [
                v.requiere_mantenimiento() for v in objetos_vehiculo
            ]
            df["estado_mantenimiento"] = df["requiere_mantenimiento"].apply(
                lambda x: "⚠️ Revisión Requerida" if x else "✅ En Regla"
            )

            return df

        except Exception as e:
            raise IOError(
                f"Error al procesar el componente de datos de flota: {e}"
            )

        