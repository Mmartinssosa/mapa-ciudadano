import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

DATA_FILE = "data.csv"
TIPOS = ["Basura", "Bache", "Luz rota"]

# Cargar datos o crear si no existe
def cargar_datos():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["tipo", "lat", "lon", "comentario", "fecha"])

# Guardar datos
def guardar_dato(nuevo_reporte):
    df = cargar_datos()
    df = pd.concat([df, pd.DataFrame([nuevo_reporte])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Interfaz Streamlit
st.title("📍 Mapa de Reportes Ciudadanos")
st.markdown("Reportá zonas con problemas de **basura**, **baches** o **luminarias**.")

with st.form("formulario"):
    tipo = st.selectbox("Tipo de problema", TIPOS)
    lat = st.number_input("Latitud", value=-34.837, format="%.6f")
    lon = st.number_input("Longitud", value=-58.379, format="%.6f")
    comentario = st.text_input("Comentario (opcional)")
    enviar = st.form_submit_button("Reportar")

    if enviar:
        nuevo = {
            "tipo": tipo,
            "lat": lat,
            "lon": lon,
            "comentario": comentario,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        guardar_dato(nuevo)
        st.success("✅ Reporte enviado con éxito.")

# Mostrar mapa
st.subheader("🗺️ Mapa con puntos reportados")
df = cargar_datos()

mapa = folium.Map(location=[-34.837, -58.379], zoom_start=14)
iconos = {
    "Basura": "trash",
    "Bache": "circle",
    "Luz rota": "lightbulb"
}

for _, row in df.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]],
        tooltip=row["tipo"],
        popup=f'{row["tipo"]} - {row["comentario"]} ({row["fecha"]})',
        icon=folium.Icon(color="blue", icon=iconos.get(row["tipo"], "info-sign"), prefix="fa")
    ).add_to(mapa)

st_data = st_folium(mapa, width=700, height=500)
