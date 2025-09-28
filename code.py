import streamlit as st
import random
import time

# -------------------------
# CONFIGURACIÓN
# -------------------------
st.set_page_config(page_title="Búsqueda de Símbolos - WAIS IV", layout="centered")

# -------------------------
# CONSTANTES
# -------------------------
SIMBOLOS = ['⊕', '⊖', '⊥', '⊃', '↻', '↷', '⊓', '⊔', '⊞', '⊠',
            '⊢', '⊣', '⊤', '⊨', '⊩', '⊬', '⊭', '⊯', '⊲', '⊳']
NUM_REACTIVOS = 10
TIEMPO_LIMITE = 120  # segundos

# -------------------------
# ESTADO INICIAL
# -------------------------
if "inicio" not in st.session_state:
    st.session_state.inicio = time.time()
    st.session_state.intento = 0
    st.session_state.correctos = 0
    st.session_state.reactivo = None
    st.session_state.seleccion_usuario = set()
    st.session_state.feedback = ""
    st.session_state.validado = False

# -------------------------
# FUNCIONES
# -------------------------
def generar_reactivo():
    objetivos = random.sample(SIMBOLOS, 2)
    busqueda = random.sample(SIMBOLOS, 5)
    presentes = [s for s in objetivos if s in busqueda]
    return {
        "objetivo": objetivos,
        "busqueda": busqueda,
        "presentes": presentes  # puede ser 0, 1 o 2 símbolos
    }

def validar_respuesta():
    seleccion = st.session_state.seleccion_usuario
    presentes = set(st.session_state.reactivo["presentes"])

    if not seleccion and not presentes:
        resultado = True
        mensaje = "✔️ Correcto. Ninguno de los símbolos estaba presente."
    elif seleccion == presentes:
        resultado = True
        mensaje = f"✔️ Correcto. Seleccionaste exactamente los símbolos presentes: {' '.join(presentes)}"
    else:
        resultado = False
        if not presentes:
            mensaje = "❌ Incorrecto. No debiste seleccionar ningún símbolo."
        else:
            mensaje = f"❌ Incorrecto. Debías seleccionar: {' '.join(presentes) if presentes else 'ninguno'}"
    return resultado, mensaje

def manejar_validacion():
    correcto, mensaje = validar_respuesta()
    if correcto:
        st.session_state.correctos += 1
    st.session_state.feedback = mensaje
    st.session_state.validado = True

def manejar_siguiente():
    st.session_state.intento += 1
    st.session_state.reactivo = generar_reactivo()
    st.session_state.seleccion_usuario = set()
    st.session_state.feedback = ""
    st.session_state.validado = False

# -------------------------
# TIEMPO RESTANTE
# -------------------------
tiempo_restante = TIEMPO_LIMITE - int(time.time() - st.session_state.inicio)

# -------------------------
# CABECERA
# -------------------------
st.title("🔍 Búsqueda de Símbolos - WAIS IV Simulado")
st.warning(f"⏱️ Tiempo restante: {tiempo_restante} segundos")

# -------------------------
# FINAL DEL JUEGO
# -------------------------
if tiempo_restante <= 0 or st.session_state.intento >= NUM_REACTIVOS:
    st.success(f"Juego terminado. Aciertos: {st.session_state.correctos} de {NUM_REACTIVOS}")
    if st.button("🔄 Reiniciar"):
        st.session_state.clear()

# -------------------------
# JUEGO EN CURSO
# -------------------------
else:
    if st.session_state.reactivo is None:
        st.session_state.reactivo = generar_reactivo()

    reactivo = st.session_state.reactivo
    objetivos = reactivo["objetivo"]
    busqueda = reactivo["busqueda"]

    st.markdown(f"### Reactivo {st.session_state.intento + 1}")
    st.markdown("#### Símbolos objetivo:")
    st.markdown(
        f"<div style='font-size: 48px; text-align: center;'>{'  '.join(objetivos)}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("#### Selecciona los símbolos que aparecen en la fila:")
    cols = st.columns(5)
    for i, simbolo in enumerate(busqueda):
        if simbolo in st.session_state.seleccion_usuario:
            if cols[i].button(f"✅ {simbolo}", key=f"select_{i}"):
                st.session_state.seleccion_usuario.remove(simbolo)
        else:
            if cols[i].button(f"{simbolo}", key=f"select_{i}"):
                st.session_state.seleccion_usuario.add(simbolo)

    st.markdown("#### O marca si **ninguno aparece**:")
    if st.button("🚫 Ninguno aparece"):
        st.session_state.seleccion_usuario = set()

    # Botón de validación
    if not st.session_state.validado:
        if st.button("✅ Validar respuesta"):
            manejar_validacion()

    # Retroalimentación
    if st.session_state.feedback:
        st.info(st.session_state.feedback)

    # Siguiente
    if st.session_state.validado:
        if st.button("➡️ Siguiente"):
            manejar_siguiente()
