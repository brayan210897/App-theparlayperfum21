import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Pro Bet Analyzer", layout="wide")
st.title("🧠 AI Pro Bet Analyzer")
st.caption("Análisis estadístico, detección de trampas y predicciones de alta fiabilidad.")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # ---------------------------------------------------------
    # EL CEREBRO AUTO-DETECTA QUÉ MODELOS TIENES DESBLOQUEADOS
    # ---------------------------------------------------------
    modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    modelo_elegido = None
    for m in modelos_disponibles:
        if '1.5-flash' in m:
            modelo_elegido = m
            break
            
    if not modelo_elegido:
        # Respaldo de seguridad por si acaso
        modelo_elegido = 'models/gemini-1.5-flash'
        
    modelo = genai.GenerativeModel(modelo_elegido)
    
except Exception as e:
    st.error("⚠️ Error de configuración con la llave. Revisa los Secrets de Streamlit.")
    st.stop()

st.subheader("1. Ingresa los Juegos o Sube Capturas")
juegos_texto = st.text_area("Escribe los equipos (1 a 10 juegos).", placeholder="Ej: Yankees vs Red Sox...")
imagenes_subidas = st.file_uploader("Sube capturas con los momios (Opcional)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("🚀 Analizar Juegos Científicamente"):
    if not juegos_texto and not imagenes_subidas:
        st.warning("Por favor ingresa texto o sube al menos una imagen de los partidos.")
    else:
        # El sistema te avisará exactamente qué motor de IA encontró y está usando
        with st.spinner(f"🧠 Analizando con el motor: {modelo_elegido}..."):
            prompt_maestro = """
            Actúa como el analista deportivo y matemático de apuestas más avanzado del mundo. 
            Analiza los juegos y/o evalúa las imágenes con los tableros de momios.
            Estructura OBLIGATORIA:
            1. 📊 CONTEXTO Y ESTADO ACTUAL: Indaga localía, clima, rachas, lesiones. Influye POSITIVA o NEGATIVAMENTE.
            2. 💸 ANÁLISIS DE MERCADO Y TRAMPAS: Analiza si hay "trampas matemáticas", valor real, y recomienda Moneyline.
            3. 🤖 RECOMENDACIONES ESTRUCTURADAS DE GEMINI AI PRO:
               - 🟢 APUESTA SEGURA (>85% fiabilidad): Máxima seguridad. Justifica.
               - 🟡 APUESTA MEDIA-ALTA (70-85% fiabilidad): Confianza verdadera. Justifica.
               - 🔴 APUESTA MEDIA (45-70% fiabilidad): Momio volátil, pero justificable. Justifica.
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
