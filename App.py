import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de diseño
st.set_page_config(page_title="AI Pro Bet Analyzer", layout="wide")
st.title("🧠 AI Pro Bet Analyzer")
st.caption("Conectado a Gemini 1.5 Pro: Análisis estadístico, detección de trampas de Las Vegas y predicciones por fiabilidad.")

Conectar con la Inteligencia Artificial (Requiere API Key)
try:
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
modelo = genai.GenerativeModel('gemini-1.5-pro')
except:
st.error("⚠️ Falta configurar tu Llave de Gemini en los Secretos de Streamlit. Sigue las instrucciones para añadirla.")
st.stop()

st.subheader("1. Ingresa los Juegos o Sube Capturas")
juegos_texto = st.text_area("Escribe los equipos (1 a 10 juegos).", placeholder="Ej: Yankees vs Red Sox, América vs Cruz Azul, Liberty vs Aces...")
imagenes_subidas = st.file_uploader("Sube capturas de Playdoit/Draftea con los momios (Opcional)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("🚀 Analizar Juegos Científicamente"):
if not juegos_texto and not imagenes_subidas:
st.warning("Por favor ingresa texto o sube al menos una imagen de los partidos.")
else:
with st.spinner("🧠 Analizando estadísticas, clima, lesiones y leyendo momios... Esto tomará unos 20 segundos."):

# EL MEGA-PROMPT QUE CONTROLA A LA IA
prompt_maestro = """
Actúa como el analista deportivo y matemático de apuestas más avanzado del mundo.
Analiza los siguientes juegos proporcionados en texto y/o evalúa las imágenes con los tableros de momios.

Tu reporte debe tener OBLIGATORIAMENTE la siguiente estructura para cada juego analizado:

1. 📊 CONTEXTO Y ESTADO ACTUAL:
Indaga y describe factores críticos: localía, clima, rachas de los últimos 5 juegos, jugadores lesionados/bajas clave, y si están peleando clasificación. Finaliza este apartado indicando si el escenario influye POSITIVA o NEGATIVAMENTE para cada equipo.

2. 💸 ANÁLISIS DE MERCADO Y TRAMPAS:
Si hay momios en la imagen o basándote en las líneas actuales de Las Vegas, analiza si hay "trampas matemáticas" (Vegas Traps), si el favorito es real o falso, y da tu recomendación de apuesta Moneyline / Favorito a ganar.

3. 🤖 RECOMENDACIONES ESTRUCTURADAS DE GEMINI AI PRO:
Basado en proyecciones matemáticas y hechos verídicos, entrega estas 3 opciones abarcando cualquier mercado disponible (Goles, Carreras, Tiros de esquina, Puntos NBA, Spreads, etc.):

- 🟢 APUESTA SEGURA (>85% fiabilidad): La opción con máxima seguridad. (Ej. Under/Over alternativo, hándicaps positivos amplios). Justifica por qué es casi infalible.
- 🟡 APUESTA MEDIA-ALTA (70-85% fiabilidad): Excelente confianza verdadera pero con un momio más jugoso. Justifica el valor estadístico.
- 🔴 APUESTA MEDIA (45-70% fiabilidad): Momio muy jugoso y volátil, pero matemáticamente justificable basada en el panorama del juego. Justifica el riesgo vs beneficio.
"""

# Recolectar datos para enviar a Gemini
inputs_para_ia = [prompt_maestro]
if juegos_texto:
inputs_para_ia.append(f"Juegos solicitados: {juegos_texto}")

if imagenes_subidas:
for img in imagenes_subidas:
imagen_procesada = Image.open(img)
inputs_para_ia.append(imagen_procesada)

# Ejecutar el análisis
try:
respuesta = modelo.generate_content(inputs_para_ia)
st.success("✅ Análisis Completado")

# Mostrar resultado
st.markdown(respuesta.text)

# Opción para compartir
st.divider()
st.subheader("📲 Compartir Estadística")
st.text_area("Copia este texto para compartir tus picks:", value=respuesta.text, height=150)

except Exception as e:
st.error(f"Error de conexión: {e}")

