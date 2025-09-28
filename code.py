import streamlit as st
import random
import time

# -------------------------
# CONFIGURACIÓN GENERAL
# -------------------------
st.set_page_config(page_title="Búsqueda de Símbolos - WAIS IV", layout="centered")

# -------------------------
# CONSTANTES DEL JUEGO
# -------------------------
SIMBOLOS = ['⊕', '⊖', '⊥', '⊃', '↻', '↷', '⊓', '⊔', '⊞', '⊠',
            '⊢', '⊣', '⊤', '⊨', '⊩', '⊬', '⊭', '⊯', '⊲', '⊳']
NUM_REACTIVOS = 10
TIEMPO_LIMITE = 120  # segundos totales del juego

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
# ENCABEZADO
# -------------------------
st.title("🔍 Búsqueda de Símbolos - WAIS IV Simulado")
st.markdown("Selecciona los símbolos que aparecen en la fila de búsqueda. Si ninguno aparece, marca la opción correspondiente. Luego presiona **Validar** para recibir retroalimentación.")
st.warning(f"⏱️ Tiempo restante: {tiempo_restante} segundos")

# -------------------------
# FIN DEL JUEGO
# -------------------------
if tiempo_restante <= 0 or st.session_state.intento >= NUM_REACTIVOS:
    st.success(f"🎯 Juego terminado. Aciertos: {st.session_state.correctos} de {NUM_REACTIVOS}")
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

    st.markdown("#### Selecciona los símbolos que aparecen en la fila de búsqueda:")
    cols = st.columns(5)
    for i, simbolo in enumerate(busqueda):
        marcado = simbolo in st.session_state.seleccion_usuario
        with cols[i]:
            if st.button(simbolo, key=f"simbolo_{i}"):
                if marcado:
                    st.session_state.seleccion_usuario.remove(simbolo)
                else:
                    st.session_state.seleccion_usuario.add(simbolo)
                st.rerun()  # Forzar actualización inmediata
            
            # Aplicar estilo visual basado en el estado de selección
            estilo = (
                "background-color: #d4f4dd; padding: 12px 16px; border-radius: 8px; font-size: 32px; border: 2px solid #4CAF50; box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);"
                if marcado else
                "background-color: #f0f0f0; padding: 12px 16px; border-radius: 8px; font-size: 32px; border: 2px solid #ccc;"
            )
            st.markdown(f"<div style='{estilo}; text-align:center; margin-top: 8px;'>{simbolo}</div>", unsafe_allow_html=True)

    st.markdown("#### O marca si **ninguno aparece**:")
    
    # Verificar si "ninguno" está seleccionado (cuando no hay símbolos seleccionados)
    ninguno_seleccionado = len(st.session_state.seleccion_usuario) == 0
    
    if st.button("🚫 Ninguno aparece"):
        st.session_state.seleccion_usuario = set()
        st.rerun()  # Forzar actualización inmediata
    
    # Mostrar el botón con estilo visual
    estilo_ninguno = (
        "background-color: #d4f4dd; padding: 12px 16px; border-radius: 8px; border: 2px solid #4CAF50; box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3); text-align: center; margin-top: 8px;"
        if ninguno_seleccionado else
        "background-color: #f0f0f0; padding: 12px 16px; border-radius: 8px; border: 2px solid #ccc; text-align: center; margin-top: 8px;"
    )
    st.markdown(f"<div style='{estilo_ninguno}'>🚫 Ninguno aparece</div>", unsafe_allow_html=True)

    # Validar
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
