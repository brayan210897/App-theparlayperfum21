
import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Pro Bet Analyzer", layout="wide")
st.title("🧠 AI Pro Bet Analyzer")
st.caption("Conectado a Gemini 1.5 Pro: Análisis estadístico y predicciones por fiabilidad.")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo = genai.GenerativeModel('gemini-1.5-pro')
except:
    st.error("⚠️ Falta configurar tu Llave de Gemini en los Secretos de Streamlit.")
    st.stop()

st.subheader("1. Ingresa los Juegos o Sube Capturas")
juegos_texto = st.text_area("Escribe los equipos (1 a 10 juegos).", placeholder="Ej: Yankees vs Red Sox, América vs Cruz Azul...")
imagenes_subidas = st.file_uploader("Sube capturas con los momios (Opcional)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("🚀 Analizar Juegos Científicamente"):
    if not juegos_texto and not imagenes_subidas:
        st.warning("Por favor ingresa texto o sube al menos una imagen de los partidos.")
    else:
        with st.spinner("🧠 Analizando estadísticas y leyendo momios..."):
            prompt_maestro = """
            Actúa como el analista deportivo y matemático de apuestas más avanzado del mundo. 
            Analiza los siguientes juegos proporcionados en texto y/o evalúa las imágenes con los tableros de momios.
            Tu reporte debe tener OBLIGATORIAMENTE la siguiente estructura para cada juego analizado:
            1. 📊 CONTEXTO Y ESTADO ACTUAL: Indaga factores críticos: localía, clima, rachas, lesiones. Influye POSITIVA o NEGATIVAMENTE.
            2. 💸 ANÁLISIS DE MERCADO Y TRAMPAS: Analiza si hay "trampas matemáticas", si el favorito es real, y recomienda Moneyline.
            3. 🤖 RECOMENDACIONES ESTRUCTURADAS DE GEMINI AI PRO:
               - 🟢 APUESTA SEGURA (>85% fiabilidad): La opción con máxima seguridad. Justifica.
               - 🟡 APUESTA MEDIA-ALTA (70-85% fiabilidad): Excelente confianza verdadera pero momio jugoso. Justifica.
               - 🔴 APUESTA MEDIA (45-70% fiabilidad): Momio muy jugoso y volátil, pero justificable. Justifica.
            """
            
            inputs_para_ia = [prompt_maestro]
            if juegos_texto:
                inputs_para_ia.append(f"Juegos solicitados: {juegos_texto}")
            
            if imagenes_subidas:
                for img in imagenes_subidas:
                    imagen_procesada = Image.open(img)
                    inputs_para_ia.append(imagen_procesada)
            
            try:
                respuesta = modelo.generate_content(inputs_para_ia)
                st.success("✅ Análisis Completado")
                st.markdown(respuesta.text)
                st.divider()
                st.subheader("📲 Compartir Estadística")
                st.text_area("Copia este texto para compartir tus picks:", value=respuesta.text, height=150)
            except Exception as e:
                st.error(f"Error de conexión: {e}")
