import streamlit as st
import random
import time

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Juego de Búsqueda de Símbolos", page_icon="🔍", layout="centered")

st.title("🔍 Juego de Búsqueda de Símbolos")
st.markdown("""
Simula la subprueba **Búsqueda de símbolos** del WAIS-IV.  
Debes responder si alguno de los símbolos objetivo aparece en el grupo de búsqueda.  
""")

# -------------------------
# PARÁMETROS DEL JUEGO
# -------------------------
SIMBOLOS = ['★', '●', '▲', '■', '◆', '☂', '✿', '♣', '☀', '♠']
NUM_REACTIVOS = 10
TIEMPO_LIMITE = 120  # segundos

# -------------------------
# GENERADOR DE REACTIVOS
# -------------------------
def generar_reactivo():
    simbolos_objetivo = random.sample(SIMBOLOS, 2)
    simbolos_busqueda = random.sample(SIMBOLOS, 5)
    hay_objetivo = any(s in simbolos_busqueda for s in simbolos_objetivo)
    return simbolos_objetivo, simbolos_busqueda, hay_objetivo

# -------------------------
# JUEGO
# -------------------------
if "inicio" not in st.session_state:
    st.session_state.inicio = time.time()
    st.session_state.intento = 0
    st.session_state.correctos = 0

# Verifica si el tiempo ya se acabó
tiempo_restante = TIEMPO_LIMITE - int(time.time() - st.session_state.inicio)
st.warning(f"⏱️ Tiempo restante: {tiempo_restante} segundos")

if tiempo_restante <= 0 or st.session_state.intento >= NUM_REACTIVOS:
    st.success(f"✅ Juego terminado. Aciertos: {st.session_state.correctos}/{NUM_REACTIVOS}")
    st.button("Reiniciar", on_click=lambda: st.session_state.clear())
else:
    simbolos_obj, simbolos_busq, es_correcto = generar_reactivo()
    st.markdown(f"### Reactivo {st.session_state.intento + 1}")
    st.markdown(f"**Símbolos objetivo:** {simbolos_obj[0]}  {simbolos_obj[1]}")
    st.markdown(f"**Símbolos de búsqueda:** {'  '.join(simbolos_busq)}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Sí"):
            if es_correcto:
                st.session_state.correctos += 1
            st.session_state.intento += 1
            st.experimental_rerun()

    with col2:
        if st.button("❌ No"):
            if not es_correcto:
                st.session_state.correctos += 1
            st.session_state.intento += 1
            st.experimental_rerun()
