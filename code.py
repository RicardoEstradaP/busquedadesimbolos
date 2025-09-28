import streamlit as st
import random
import time

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Búsqueda de Símbolos", page_icon="🔍", layout="centered")

# -------------------------
# CONSTANTES Y VARIABLES
# -------------------------
SIMBOLOS = ['⊕', '⊖', '⊥', '⊃', '↻', '↷', '⊓', '⊔', '⊞', '⊠',
            '⊢', '⊣', '⊤', '⊨', '⊩', '⊬', '⊭', '⊯', '⊲', '⊳']
NUM_REACTIVOS = 10
TIEMPO_LIMITE = 120  # segundos

# -------------------------
# INICIALIZACIÓN
# -------------------------
if "inicio" not in st.session_state:
    st.session_state.inicio = time.time()
    st.session_state.intento = 0
    st.session_state.correctos = 0
    st.session_state.reactivo = None
    st.session_state.seleccion_usuario = []

# -------------------------
# FUNCIONES
# -------------------------
def generar_reactivo():
    objetivos = random.sample(SIMBOLOS, 2)
    busqueda = random.sample(SIMBOLOS, 5)
    return {
        "objetivo": objetivos,
        "busqueda": busqueda
    }

def validar_respuesta():
    seleccion = st.session_state.seleccion_usuario
    objetivos = st.session_state.reactivo["objetivo"]
    busqueda = st.session_state.reactivo["busqueda"]

    # El usuario debe haber seleccionado solo 1 o 0 símbolos (como en el test real)
    if len(seleccion) > 1:
        return False  # Se penaliza la selección múltiple
    elif len(seleccion) == 0 and not any(o in busqueda for o in objetivos):
        return True
    elif len(seleccion) == 1 and seleccion[0] in objetivos and seleccion[0] in busqueda:
        return True
    else:
        return False

def manejar_siguiente():
    if validar_respuesta():
        st.session_state.correctos += 1
    st.session_state.intento += 1
    st.session_state.reactivo = generar_reactivo()
    st.session_state.seleccion_usuario = []

# -------------------------
# TIEMPO RESTANTE
# -------------------------
tiempo_restante = TIEMPO_LIMITE - int(time.time() - st.session_state.inicio)

# -------------------------
# CABECERA
# -------------------------
st.title("🔍 Búsqueda de Símbolos - WAIS IV Simulado")
st.markdown("Selecciona el símbolo que aparece en la fila de búsqueda. Si no aparece ninguno, deja sin seleccionar y presiona **Validar**.")

st.warning(f"⏱️ Tiempo restante: {tiempo_restante} segundos")

# -------------------------
# FINAL DEL JUEGO
# -------------------------
if tiempo_restante <= 0 or st.session_state.intento >= NUM_REACTIVOS:
    st.success(f"Juego terminado. Aciertos: {st.session_state.correctos} de {NUM_REACTIVOS}")
    if st.button("🔄 Reiniciar juego"):
        st.session_state.clear()

# -------------------------
# JUEGO EN CURSO
# -------------------------
else:
    if st.session_state.reactivo is None:
        st.session_state.reactivo = generar_reactivo()

    reactivo = st.session_state.reactivo

    st.markdown(f"### Reactivo {st.session_state.intento + 1}")
    st.markdown("#### Símbolos Objetivo:")
    st.markdown(f"<div style='font-size: 48px; text-align: center;'>{'  '.join(reactivo['objetivo'])}</div>", unsafe_allow_html=True)

    st.markdown("#### Símbolos de Búsqueda:")
    cols = st.columns(5)
    for idx, simbolo in enumerate(reactivo["busqueda"]):
        if cols[idx].button(f"{simbolo}", key=f"simbolo_{idx}"):
            st.session_state.seleccion_usuario = [simbolo]  # Solo una selección permitida

    st.markdown("----")
    st.markdown("¿Ya terminaste tu selección?")
    if st.button("✅ Validar"):
        manejar_siguiente()
