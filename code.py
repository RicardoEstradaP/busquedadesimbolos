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
            '⊢', '⊣', '⊤', '⊨', '⊩', '⊬', '⊭', '⊯', '◀', '▶']
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
    st.session_state.juego_iniciado = False
    st.session_state.resultados = []  # Para guardar los resultados de cada reactivo

# -------------------------
# FUNCIONES
# -------------------------
def generar_reactivo():
    objetivos = random.sample(SIMBOLOS, 2)
    
    # Decidir aleatoriamente cuántos símbolos objetivos aparecerán (0, 1 o 2)
    num_presentes = random.choice([0, 1, 2])
    
    if num_presentes == 0:
        presentes = []
        # Generar 5 símbolos aleatorios que NO sean los objetivos
        simbolos_disponibles = [s for s in SIMBOLOS if s not in objetivos]
        busqueda = random.sample(simbolos_disponibles, 5)
    elif num_presentes == 1:
        presentes = [random.choice(objetivos)]
        # Generar 4 símbolos aleatorios + 1 objetivo
        simbolos_disponibles = [s for s in SIMBOLOS if s not in objetivos]
        otros_simbolos = random.sample(simbolos_disponibles, 4)
        busqueda = otros_simbolos + presentes
        random.shuffle(busqueda)  # Mezclar para que no esté siempre al final
    else:  # num_presentes == 2
        presentes = objetivos.copy()
        # Generar 3 símbolos aleatorios + 2 objetivos
        simbolos_disponibles = [s for s in SIMBOLOS if s not in objetivos]
        otros_simbolos = random.sample(simbolos_disponibles, 3)
        busqueda = otros_simbolos + presentes
        random.shuffle(busqueda)  # Mezclar para que no estén siempre al final
    
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
    
    # Guardar el resultado del reactivo actual
    resultado_reactivo = {
        "reactivo_num": st.session_state.intento + 1,
        "objetivos": st.session_state.reactivo["objetivo"],
        "busqueda": st.session_state.reactivo["busqueda"],
        "presentes": st.session_state.reactivo["presentes"],
        "seleccion_usuario": list(st.session_state.seleccion_usuario),
        "ninguno_seleccionado": st.session_state.ninguno_seleccionado,
        "correcto": correcto,
        "mensaje": mensaje
    }
    st.session_state.resultados.append(resultado_reactivo)
    
    st.session_state.validado = True

def manejar_siguiente():
    st.session_state.intento += 1
    st.session_state.reactivo = generar_reactivo()
    st.session_state.seleccion_usuario = set()
    st.session_state.ninguno_seleccionado = False
    st.session_state.validado = False

# -------------------------
# PANTALLA DE INSTRUCCIONES
# -------------------------
if not st.session_state.juego_iniciado:
    st.title("🔍 Búsqueda de Símbolos - WAIS IV Simulado")
    
    st.markdown("""
    <div style="background-color: #f0f8ff; padding: 30px; border-radius: 15px; border: 2px solid #4CAF50; margin: 20px 0;">
        <h2 style="color: #2c3e50; text-align: center; margin-bottom: 25px;">📋 Instrucciones</h2>
        <p style="font-size: 18px; line-height: 1.6; color: #34495e;">
            <strong>En esta tarea, vas a ver dos símbolos aquí a la izquierda. Luego, verás un grupo de cinco símbolos. 
            Tu trabajo consiste en ver si uno de los dos símbolos de la izquierda aparece en el grupo de cinco símbolos de la derecha.</strong>
        </p>
        <br>
        <p style="font-size: 18px; line-height: 1.6; color: #34495e;">
            <strong>Si uno de los símbolos aparece, selecciona el símbolo correspondiente. Si ninguno aparece, selecciona "Ninguno aparece". 
            Hazlo lo más rápido que puedas sin cometer errores.</strong>
        </p>
        <br>
        <p style="font-size: 20px; text-align: center; color: #e74c3c; font-weight: bold;">
            ¿Está claro?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ¡Comenzar!", key="iniciar_juego", use_container_width=True):
            st.session_state.juego_iniciado = True
            st.session_state.inicio = time.time()  # Reiniciar el tiempo cuando comience el juego
            st.rerun()
    
    st.stop()  # Detener la ejecución aquí hasta que se inicie el juego

# -------------------------
# TIEMPO RESTANTE
# -------------------------
tiempo_restante = TIEMPO_LIMITE - int(time.time() - st.session_state.inicio)

# -------------------------
# ENCABEZADO
# -------------------------
st.title("🔍 Búsqueda de Símbolos - WAIS IV Simulado")
st.markdown("Selecciona los símbolos que aparecen en la fila de búsqueda. Si ninguno aparece, marca la opción correspondiente. Luego presiona **Validar** para recibir retroalimentación.")

# Temporizador grande y en tiempo real
if tiempo_restante > 0:
    # Color del temporizador según el tiempo restante
    if tiempo_restante <= 10:
        color = "🔴"  # Rojo para los últimos 10 segundos
    elif tiempo_restante <= 20:
        color = "🟡"  # Amarillo para los últimos 20 segundos
    else:
        color = "🟢"  # Verde para el resto del tiempo
    
    st.markdown(f"""
    <div style="text-align: center; font-size: 48px; font-weight: bold; margin: 20px 0; padding: 20px; border: 3px solid #333; border-radius: 15px; background-color: #f0f0f0;">
        {color} {tiempo_restante} segundos
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; font-size: 48px; font-weight: bold; margin: 20px 0; padding: 20px; border: 3px solid #ff0000; border-radius: 15px; background-color: #ffebee;">
        ⏰ Tiempo agotado
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# FIN DEL JUEGO
# -------------------------
if tiempo_restante <= 0 or st.session_state.intento >= NUM_REACTIVOS:
    st.success(f"🎯 Juego terminado. Aciertos: {st.session_state.correctos} de {st.session_state.intento}")
    
    # Mostrar resultados detallados
    st.markdown("### 📊 Resultados Detallados")
    
    for resultado in st.session_state.resultados:
        with st.expander(f"Reactivo {resultado['reactivo_num']} - {'✅ Correcto' if resultado['correcto'] else '❌ Incorrecto'}"):
            st.markdown(f"**Símbolos objetivo:** {' '.join(resultado['objetivos'])}")
            st.markdown(f"**Fila de búsqueda:** {' '.join(resultado['busqueda'])}")
            st.markdown(f"**Símbolos presentes:** {' '.join(resultado['presentes']) if resultado['presentes'] else 'Ninguno'}")
            
            if resultado['ninguno_seleccionado']:
                st.markdown(f"**Tu selección:** Ninguno aparece")
            else:
                st.markdown(f"**Tu selección:** {' '.join(resultado['seleccion_usuario']) if resultado['seleccion_usuario'] else 'Ninguno'}")
            
            if not resultado['correcto']:
                st.error(f"**Error:** {resultado['mensaje']}")
            else:
                st.success("**¡Correcto!**")
    
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

    # Botón siguiente (solo aparece después de validar)
    if st.session_state.validado:
        if st.button("➡️ Siguiente"):
            manejar_siguiente()
            st.rerun()
    
    # Auto-refresh para el temporizador (solo si el juego está en curso y no hay validación pendiente)
    if (tiempo_restante > 0 and 
        st.session_state.intento < NUM_REACTIVOS and 
        not st.session_state.validado and 
        not st.session_state.feedback):
        time.sleep(1)  # Actualizar cada segundo
        st.rerun()
