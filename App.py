import streamlit as st

st.set_page_config(page_title="Analizador Deportivo AI", layout="centered")

st.title("⚽ Analytics Pro: Odds & Predictions")
st.caption("Sistema de análisis estadístico y estimación de probabilidades")

# Sección 1: Selección de deporte e ingreso de datos
st.subheader("1. Datos del Partido")
deporte = st.selectbox("Deporte / Liga", ["Fútbol (Liga MX, Europa, etc.)", "Béisbol (MLB)", "Baloncesto (NBA/WNBA)", "Tenis", "NFL"])
partido = st.text_input("Partido o Evento", placeholder="Ej: América vs Chivas o Yankees vs Red Sox")
momio = st.number_input("Momio / Cuota disponible (Ej: 1.35 o -280)", min_value=1.01, value=1.35, step=0.05)

# Sección 2: Carga de imagen o notas adicionales
st.subheader("2. Contexto o Captura de Pantalla")
foto_partido = st.file_uploader("Sube foto de alineaciones, clima o momios (Opcional)", type=["jpg", "png", "jpeg"])
notas = st.text_area("Bajas, clima o detalles extra", placeholder="Ej: Lluvia fuerte esperada, delantero estrella lesionado...")

# Sección 3: Calculadora de Probabilidad de Cobertura
st.subheader("3. Probabilidad Estimada")
prob_estimada = st.slider("Ajusta la probabilidad estimada por la IA (%)", 40, 95, 80)

# Lógica de clasificación
def evaluar_confianza(prob):
    if prob >= 80:
        return "🔥 ALTA / SÚPER CONFIABLE", "st.success"
    elif prob >= 75:
        return "🟢 MEDIA-ALTA", "st.info"
    elif prob >= 65:
        return "🟡 MEDIA", "st.warning"
    else:
        return "🔴 BAJA / RIESGO ELEVADO", "st.error"

nivel, tipo_alerta = evaluar_confianza(prob_estimada)

st.markdown(f"### Nivel de Confianza: **{nivel}**")

# Botón para generar recomendación final
if st.button("Generar Dictamen de Apuesta"):
    st.divider()
    st.subheader("📋 Resumen Ejecutivo")
    st.write(f"**Deporte:** {deporte}")
    st.write(f"**Evento:** {partido if partido else 'No especificado'}")
    st.write(f"**Momio evaluado:** {momio:.2f}x")
    st.write(f"**Probabilidad asignada:** {prob_estimada}%")
    
    if momio >= 1.30 and prob_estimada >= 80:
        st.success("✅ **RECOMENDACIÓN:** La selección cumple con los criterios de alta seguridad (>=80%) y cuota viable (>=1.30x).")
    else:
        st.warning("⚠️ **ADVERTENCIA:** La selección no alcanza el umbral de rendimiento o la relación riesgo/beneficio es ajustada.")
