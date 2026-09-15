import streamlit as st
import folium
import streamlit.components.v1 as components
from componente_datos import obtener_vehiculos

st.set_page_config(page_title="Gestión de Flota", layout="wide")
st.title("Sistema de Gestión de Mantenimiento de Flota")

# 1. Cargar la flota de vehículos POO desde el módulo de datos
@st.cache_data
def cargar_flota():
    return obtener_vehiculos()

vehiculos = cargar_flota()

# 2. Panel Lateral de Evaluación
st.sidebar.header("Evaluación de Mantenimiento")
opciones = {f"{v.id} - {v.modelo}": v for v in vehiculos}
seleccion_label = st.sidebar.selectbox("Selecciona un vehículo:", list(opciones.keys()))
vehiculo_seleccionado = opciones[seleccion_label]

st.sidebar.subheader("Detalles Técnicos")
st.sidebar.write(f"**Identificador:** {vehiculo_seleccionado.id}")
st.sidebar.write(f"**Modelo:** {vehiculo_seleccionado.modelo}")
st.sidebar.write(f"**Tipo:** {type(vehiculo_seleccionado).__name__}")
st.sidebar.write(f"**Kilometraje:** {vehiculo_seleccionado.kilometraje} km")

# Evaluación polimórfica según la subclase
if vehiculo_seleccionado.requiere_mantenimiento():
    st.sidebar.error("Estado: REQUIERE TALLER")
else:
    st.sidebar.success("Estado: OPERATIVO")

# 3. Visualización del Mapa
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Ubicación de Unidades")
    m = folium.Map(location=[42.8467, -2.6716], zoom_start=13)

    for v in vehiculos:
        color_marker = "red" if v.requiere_mantenimiento() else "green"
        popup_info = f"<b>{v.id}</b><br>Modelo: {v.modelo}<br>Tipo: {type(v).__name__}<br>KM: {v.kilometraje}"

        folium.Marker(
            location=[v.lat, v.lng],
            popup=popup_info,
            tooltip=f"{v.id} ({v.modelo})",
            icon=folium.Icon(color=color_marker, icon="car", prefix="fa")
        ).add_to(m)

    # Renderizado HTML nativo para prevenir pantallas negras
    mapa_html = m._repr_html_()
    components.html(mapa_html, height=450, scrolling=False)

with col2:
    st.subheader("Resumen de la Flota")
    total_vehiculos = len(vehiculos)
    en_taller = sum(1 for v in vehiculos if v.requiere_mantenimiento())
    
    st.metric(label="Total Vehículos", value=total_vehiculos)
    st.metric(label="Requieren Taller", value=en_taller, delta_color="inverse")

    

