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
    st.session_state.ninguno_seleccionado = False
    st.session_state.feedback = ""
    st.session_state.validado = False

# -------------------------
# FUNCIONES
# -------------------------
def generar_reactivo():
    objetivos = random.sample(SIMBOLOS, 2)
    busqueda = random.sample(SIMBOLOS, 5)
    
    # Decidir aleatoriamente cuántos símbolos objetivos aparecerán (0, 1 o 2)
    num_presentes = random.choice([0, 1, 2])
    
    if num_presentes == 0:
        presentes = []
    elif num_presentes == 1:
        presentes = [random.choice(objetivos)]
    else:  # num_presentes == 2
        presentes = objetivos.copy()
    
    # Asegurar que los símbolos presentes estén en la fila de búsqueda
    for simbolo in presentes:
        if simbolo not in busqueda:
            # Reemplazar un símbolo aleatorio en busqueda con el objetivo
            busqueda[random.randint(0, 4)] = simbolo
    
    return {
        "objetivo": objetivos,
        "busqueda": busqueda,
        "presentes": presentes
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
    st.session_state.ninguno_seleccionado = False
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
            # Aplicar estilo al botón directamente
            if marcado:
                st.markdown("""
                <style>
                div[data-testid="column"]:nth-of-type({}) button {{
                    background-color: #d4f4dd !important;
                    border: 2px solid #4CAF50 !important;
                    box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3) !important;
                }}
                </style>
                """.format(i+1), unsafe_allow_html=True)
            
            if st.button(simbolo, key=f"simbolo_{i}"):
                if marcado:
                    st.session_state.seleccion_usuario.remove(simbolo)
                else:
                    st.session_state.seleccion_usuario.add(simbolo)
                st.session_state.ninguno_seleccionado = False  # Desmarcar "ninguno" si se selecciona un símbolo
                st.rerun()  # Forzar actualización inmediata

    st.markdown("#### O marca si **ninguno aparece**:")
    
    # Aplicar estilo al botón "Ninguno aparece" si está seleccionado
    if st.session_state.ninguno_seleccionado:
        st.markdown("""
        <style>
        button[kind="secondary"]:has-text("🚫 Ninguno aparece") {
            background-color: #d4f4dd !important;
            border: 2px solid #4CAF50 !important;
            box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    if st.button("🚫 Ninguno aparece"):
        st.session_state.seleccion_usuario = set()
        st.session_state.ninguno_seleccionado = True
        st.rerun()  # Forzar actualización inmediata

    # Botón de validación
    if not st.session_state.validado:
        if st.button("✅ Validar respuesta"):
            manejar_validacion()
            st.rerun()

    # Retroalimentación
    if st.session_state.feedback:
        st.info(st.session_state.feedback)

    # Botón siguiente
    if st.session_state.validado:
        if st.button("➡️ Siguiente"):
            manejar_siguiente()
            st.rerun()
