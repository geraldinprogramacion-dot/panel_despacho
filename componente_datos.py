import pandas as pd
from datetime import datetime

class IngestorDatos:
    """Componente independiente para la ingesta, limpieza y validacion de datos de la flota."""
    
    def __init__(self):
        pass

    def cargar_datos_flota(self) -> pd.DataFrame:
        """ 
        Genera y valida el DataFrame base de la empresa con los 3 vehiculos requeridos.
        Aplica limpieza de tipos de datos y cálculo polimórfico de mantenimiento.
        """
        try:
            # 1. Creación del DataFrame con los 3 vehículos específicos de la empresa
            datos_raw = [
                {
                    'id': 'V-001',
                    'matricula': '4821-KBC',
                    'modelo': 'Mercedes Vito Tourer 2016',
                    'tipo': 'Furgoneta',
                    'kilometraje': 16200,
                    'lat': 42.8467,
                    'lng': -2.6716
                },
                {
                    'id': 'V-002',
                    'matricula': '9102-LMN',
                    'modelo': 'Renault Master 2021',
                    'tipo': 'Furgoneta',
                    'kilometraje': 11400,
                    'lat': 42.8520,
                    'lng': -2.6810
                },
                {
                    'id': 'E-001',
                    'matricula': '3341-NXZ',
                    'modelo': 'Nissan Townstar EV 2023',
                    'tipo': 'Electrico',
                    'kilometraje': 5300,
                    'lat': 42.8412,
                    'lng': -2.6650
                }
            ]
            
            df = pd.DataFrame(datos_raw)

            # 2. Validación del contrato de la interfaz (columnas requeridas)
            columnas_requeridas = {'id', 'matricula', 'modelo', 'tipo', 'kilometraje', 'lat', 'lng'}
            if not columnas_requeridas.issubset(df.columns):
                raise ValueError(f"El conjunto de datos no cumple el contrato. Columnas requeridas: {columnas_requeridas}")

            # 3. Limpieza y conversión de tipos de datos
            df['kilometraje'] = df['kilometraje'].astype(int)
            df['lat'] = df['lat'].astype(float)
            df['lng'] = df['lng'].astype(float)

            # 4. Evaluación Polimórfica de Mantenimiento
            # Furgonetas: >= 15000 km | Eléctricos: >= 5000 km
            def evaluar_mantenimiento(row):
                if row['tipo'] == 'Furgoneta':
                    return row['kilometraje'] >= 15000
                elif row['tipo'] == 'Electrico':
                    return row['kilometraje'] >= 5000
                return False

            df['requiere_mantenimiento'] = df.apply(evaluar_mantenimiento, axis=1)
            df['estado_mantenimiento'] = df['requiere_mantenimiento'].apply(
                lambda x: '⚠️ Revisión Requerida' if x else '✅ En Regla'
            )

            return df

        except Exception as e:
            raise IOError(f"Error al procesar el componente de datos de flota: {e}")

# --- PRUEBA DEL COMPONENTE ---
if __name__ == '__main__':
    ingestor = IngestorDatos()
    df_flota = ingestor.cargar_datos_flota()
    print(df_flota[['id', 'modelo', 'kilometraje', 'estado_mantenimiento']])
    