import streamlit as st
import folium
import streamlit.components.v1 as components
from componente_datos import obtener_vehiculos

st.title("Panel de Despacho y Mantenimiento")

# --- LOGIN BÁSICO ---
# Creamos un estado de sesión para controlar si está logueado
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.subheader("Por favor, inicia sesión")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Entrar"):
        # Contraseña y usuario súper sencillos para un entorno escolar
        if usuario == "admin" and password == "1234":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    # --- APLICACIÓN PRINCIPAL (Si ya inició sesión) ---
    st.success("¡Bienvenido al sistema!")
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()

    st.write("Seguimiento y control de flota académica.")
    
    vehiculos = obtener_vehiculos()
    m = folium.Map(location=[42.8467, -2.6716], zoom_start=13)

    for v in vehiculos:
        color_marcador = "green" if v.estado == "Operativo" else "red"
        texto_popup = f"<b>Placa:</b> {v.placa}<br><b>Tipo:</b> {v.detalles_especificos()}<br><b>Estado:</b> {v.estado}"
        
        folium.Marker(
            location=[v.lat, v.lon],
            popup=texto_popup,
            icon=folium.Icon(color=color_marcador, icon="info-sign")
        ).add_to(m)

    components.html(m._repr_html_(), height=500)

    