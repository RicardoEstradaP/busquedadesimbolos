import streamlit as st
import random
import time

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Juego de Búsqueda de Símbolos", page_icon="🔍", layout="centered")

# -------------------------
# CONSTANTES Y VARIABLES
# -------------------------
SIMBOLOS = ['★', '●', '▲', '■', '◆', '☂', '✿', '♣', '☀', '♠']
NUM_REACTIVOS = 10
TIEMPO_LIMITE = 120  # segundos

# -------------------------
# INICIALIZACIÓN DE ESTADO
# -------------------------
if "inicio" not in st.session_state:
    st.session_state.inicio = time.time()
    st.session_state.intento = 0
    st.session_state.correctos = 0
    st.session_state.reactivo = None

# -------------------------
# FUNCIONES DEL JUEGO
# -------------------------
def generar_reactivo():
    simbolos_objetivo = random.sample(SIMBOLOS, 2)
    simbolos_busqueda = random.sample(SIMBOLOS, 5)
    hay_objetivo = any(s in simbolos_busqueda for s in simbolos_objetivo)
    return {
        "objetivo": simbolos_objetivo,
        "busqueda": simbolos_busqueda,
        "es_correcto": hay_objetivo
    }

def manejar_respuesta(respuesta_usuario):
    reactivo = st.session_state.reactivo
    if (respuesta_usuario and reactivo["es_correcto"]) or (not respuesta_usuario and not reactivo["es_correcto"]):
        st.session_state.correctos += 1
    st.session_state.intento += 1
    st.session_state.reactivo = generar_reactivo()

# -------------------------
# JUEGO EN CURSO
# -------------------------
st.title("🔍 Juego de Búsqueda de Símbolos")
st.markdown("Responde si alguno de los símbolos objetivo aparece en el grupo de búsqueda.")

# Verificar tiempo restante
tiempo_restante = TIEMPO_LIMITE - int(time.time() - st.session_state.inicio)
st.warning(f"⏱️ Tiempo restante: {tiempo_restante} segundos")

# Fin del juego
if tiempo_restante <= 0 or st.session_state.intento >= NUM_REACTIVOS:
    st.success(f"Juego terminado. Aciertos: {st.session_state.correctos} de {NUM_REACTIVOS}")
    if st.button("🔄 Reiniciar juego"):
        st.session_state.clear()
else:
    if st.session_state.reactivo is None:
        st.session_state.reactivo = generar_reactivo()

    reactivo = st.session_state.reactivo

    st.markdown(f"### Reactivo {st.session_state.intento + 1}")
    st.markdown(f"**Símbolos objetivo:** {reactivo['objetivo'][0]}  {reactivo['objetivo'][1]}")
    st.markdown(f"**Símbolos de búsqueda:** {'  '.join(reactivo['busqueda'])}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Sí, aparece"):
            manejar_respuesta(True)

    with col2:
        if st.button("❌ No aparece"):
            manejar_respuesta(False)
