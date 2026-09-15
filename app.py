import streamlit as st
import folium
from streamlit_folium import st_folium

# Ejemplo de función para renderizar el mapa interactivo
def mostrar_mapa_interactivo(lista_vehiculos):
    # 1. Crear el mapa centrado en una ubicación inicial
    m = folium.Map(location=[-33.45, -70.66], zoom_start=12)

    # 2. Agregar los vehículos como marcadores
    for v in lista_vehiculos:
        folium.Marker(
            location=[v.lat, v.lng],
            popup=v.matricula,
            tooltip=f"{v.modelo} ({v.matricula})",
            # Guardamos la matrícula en el objeto para identificarlo al hacer clic
            icon=folium.Icon(color="blue" if v.necesita_mantenimiento() else "green")
        ).add_to(m)

    # 3. Renderizar el mapa en Streamlit y capturar eventos de clic
    map_data = st_folium(m, width=700, height=500)

    # 4. Capturar el clic en un marcador
    if map_data and map_data.get("last_object_clicked"):
        click_coords = map_data["last_object_clicked"]
        lat_clic = click_coords["lat"]
        lng_clic = click_coords["lng"]

        # Buscar el objeto vehículo correspondiente a esas coordenadas
        vehiculo_seleccionado = next(
            (v for v in lista_vehiculos if abs(v.lat - lat_clic) < 0.0001 and abs(v.lng - lng_clic) < 0.0001),
            None
        )

        # 5. Mostrar la evaluación del vehículo seleccionado
        if vehiculo_seleccionado:
            st.subheader(f"Vehículo Seleccionado: {vehiculo_seleccionado.matricula}")
            st.write(f"Modelo: {vehiculo_seleccionado.modelo}")
            st.write(f"Kilometraje: {vehiculo_seleccionado.kilometraje} km")

            # Evaluación polimórfica llamando al método de tu clase POO
            if vehiculo_seleccionado.necesita_mantenimiento():
                st.error("⚠️ Estado: REQUIERE TALLER")
            else:
                st.success("✅ Estado: OPERATIVO")

