# app.py - PARTE 1

import streamlit as st
import json
import random
import time
from datetime import datetime

st.set_page_config(
page_title="Grammar Quest",
page_icon="📚",
layout="wide"
)

# ======================================

# ESTILOS

# ======================================

st.markdown("""

<style>
.main {
    padding-top: 1rem;
}

.level-card {
    padding:15px;
    border-radius:12px;
    border:1px solid #ddd;
    margin-bottom:10px;
}

.big-title{
    text-align:center;
    color:#2563eb;
}

.success-box{
    padding:15px;
    border-radius:10px;
    background:#dcfce7;
}

.error-box{
    padding:15px;
    border-radius:10px;
    background:#fee2e2;
}
</style>

""", unsafe_allow_html=True)

# ======================================

# CARGAR JSON

# ======================================

@st.cache_data
def cargar_preguntas():
with open("preguntas.json", "r", encoding="utf-8") as f:
data = json.load(f)

niveles = {}

for clave, valor in data.items():
    niveles[int(clave)] = valor

return niveles

niveles = cargar_preguntas()

# ======================================

# SESSION STATE

# ======================================

if "nombre" not in st.session_state:
st.session_state.nombre = ""

if "nivel_actual" not in st.session_state:
st.session_state.nivel_actual = None

if "pantalla" not in st.session_state:
st.session_state.pantalla = "menu"

if "desbloqueados" not in st.session_state:
st.session_state.desbloqueados = [1]

if "preguntas_actuales" not in st.session_state:
st.session_state.preguntas_actuales = []

if "indice" not in st.session_state:
st.session_state.indice = 0

if "puntaje" not in st.session_state:
st.session_state.puntaje = 0

if "respondida" not in st.session_state:
st.session_state.respondida = False

if "respuesta_usuario" not in st.session_state:
st.session_state.respuesta_usuario = ""

if "inicio_pregunta" not in st.session_state:
st.session_state.inicio_pregunta = None

if "estadisticas" not in st.session_state:
st.session_state.estadisticas = {}

# ======================================

# FUNCIONES

# ======================================

def abrir_nivel(nivel):
st.session_state.nivel_actual = nivel
st.session_state.pantalla = "instrucciones"

def comenzar_nivel():

datos = niveles[st.session_state.nivel_actual]

st.session_state.preguntas_actuales = random.sample(
    datos["preguntas"],
    datos["cantidad"]
)

st.session_state.indice = 0
st.session_state.puntaje = 0
st.session_state.respondida = False
st.session_state.inicio_pregunta = time.time()

st.session_state.pantalla = "juego"
```

def volver_menu():
st.session_state.pantalla = "menu"

# ======================================

# HEADER

# ======================================

st.markdown(
"<h1 class='big-title'>📚 Grammar Quest</h1>",
unsafe_allow_html=True
)

# ======================================

# MENU

# ======================================

if st.session_state.pantalla == "menu":

st.markdown("### Interactive English Learning Platform")

nombre = st.text_input(
    "Student Name",
    value=st.session_state.nombre
)

st.session_state.nombre = nombre

st.divider()

st.subheader("🎯 Select a Level")

cols = st.columns(2)

contador = 0

for nivel, datos in niveles.items():

    with cols[contador % 2]:

        desbloqueado = nivel in st.session_state.desbloqueados

        estado = "✅ Unlocked" if desbloqueado else "🔒 Locked"

        st.markdown(
            f"""
            <div class='level-card'>
            <h4>Level {nivel}</h4>
            <b>{datos['nombre']}</b><br>
            {estado}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.button(
            f"Open Level {nivel}",
            disabled=not desbloqueado,
            key=f"lvl{nivel}",
            on_click=abrir_nivel,
            args=(nivel,)
        )

    contador += 1

# ======================================

# INSTRUCCIONES

# ======================================

elif st.session_state.pantalla == "instrucciones":

datos = niveles[st.session_state.nivel_actual]

st.subheader(
    f"Level {st.session_state.nivel_actual} - {datos['nombre']}"
)

st.info(datos["descripcion"])

c1, c2, c3 = st.columns(3)

c1.metric(
    "Questions",
    datos["cantidad"]
)

c2.metric(
    "Time",
    f"{datos['tiempo']} sec"
)

c3.metric(
    "Minimum Score",
    f"{datos['minimo']}%"
)

st.divider()

if st.button(
    "🚀 Start Level",
    use_container_width=True
):
    comenzar_nivel()

if st.button(
    "⬅ Back",
    use_container_width=True
):
    volver_menu()
```
# ======================================

# JUEGO

# ======================================

elif st.session_state.pantalla == "juego":

datos_nivel = niveles[st.session_state.nivel_actual]

preguntas = st.session_state.preguntas_actuales

indice = st.session_state.indice

total = len(preguntas)

progreso = indice / total

st.progress(progreso)

st.markdown(
    f"### Question {indice + 1} of {total}"
)

pregunta_actual = preguntas[indice]

# ==========================
# TEMPORIZADOR
# ==========================

tiempo_limite = datos_nivel["tiempo"]

if st.session_state.inicio_pregunta is None:
    st.session_state.inicio_pregunta = time.time()

transcurrido = int(
    time.time() - st.session_state.inicio_pregunta
)

restante = tiempo_limite - transcurrido

if restante < 0:
    restante = 0

c1, c2 = st.columns([3, 1])

with c1:
    st.info(
        f"Level {st.session_state.nivel_actual} - {datos_nivel['nombre']}"
    )

with c2:
    st.metric(
        "⏱ Time",
        f"{restante}s"
    )

# ==========================
# TIEMPO AGOTADO
# ==========================

if restante == 0 and not st.session_state.respondida:

    st.session_state.respondida = True

    st.error("⏰ Time's up!")

    st.session_state.respuesta_usuario = ""

    st.rerun()

# ==========================
# PREGUNTA
# ==========================

st.markdown("---")

st.subheader(
    pregunta_actual["pregunta"]
)

respuesta_correcta = pregunta_actual["respuesta"]

# ==========================
# OPCIONES
# ==========================

if not st.session_state.respondida:

    opcion = st.radio(
        "Choose an answer:",
        pregunta_actual["opciones"],
        key=f"pregunta_{indice}"
    )

    if st.button(
        "✅ Confirm Answer",
        use_container_width=True
    ):

        st.session_state.respondida = True

        st.session_state.respuesta_usuario = opcion

        if opcion == respuesta_correcta:
            st.session_state.puntaje += 1

        st.rerun()

# ==========================
# MOSTRAR RESULTADO
# ==========================

else:

    respuesta_usuario = st.session_state.respuesta_usuario

    if respuesta_usuario == respuesta_correcta:

        st.success("✅ Correct!")

    elif respuesta_usuario == "":

        st.error(
            f"⏰ Time's up! Correct answer: {respuesta_correcta}"
        )

    else:

        st.error(
            f"❌ Incorrect! Correct answer: {respuesta_correcta}"
        )

    st.info(
        pregunta_actual["explicacion"]
    )

    porcentaje_actual = round(
        (st.session_state.puntaje / (indice + 1)) * 100
    )

    st.metric(
        "Current Score",
        f"{porcentaje_actual}%"
    )

    # ======================
    # SIGUIENTE
    # ======================

    if st.button(
        "➡ Next Question",
        use_container_width=True
    ):

        st.session_state.indice += 1

        st.session_state.respondida = False

        st.session_state.respuesta_usuario = ""

        st.session_state.inicio_pregunta = time.time()

        # FIN DEL NIVEL
        if st.session_state.indice >= total:

            st.session_state.pantalla = "resultado"

        st.rerun()

# ==========================
# AUTO REFRESH TEMPORIZADOR
# ==========================

if not st.session_state.respondida:
    time.sleep(1)
    st.rerun()

# ======================================

# RESULTADOS

# ======================================

elif st.session_state.pantalla == "resultado":

```
datos_nivel = niveles[st.session_state.nivel_actual]

total = len(st.session_state.preguntas_actuales)

puntaje = st.session_state.puntaje

porcentaje = round(
    (puntaje / total) * 100
)

minimo = datos_nivel["minimo"]

st.markdown("# 🏆 Final Result")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Correct Answers",
    f"{puntaje}/{total}"
)

c2.metric(
    "Percentage",
    f"{porcentaje}%"
)

c3.metric(
    "Required",
    f"{minimo}%"
)

# ==========================
# MEDALLAS
# ==========================

medalla = "🎖 Participant"

if porcentaje >= 90:
    medalla = "🥇 Gold Medal"

elif porcentaje >= 80:
    medalla = "🥈 Silver Medal"

elif porcentaje >= 70:
    medalla = "🥉 Bronze Medal"

st.markdown("## " + medalla)

# ==========================
# GUARDAR ESTADÍSTICAS
# ==========================

st.session_state.estadisticas[
    st.session_state.nivel_actual
] = porcentaje

# ==========================
# APROBADO
# ==========================

if porcentaje >= minimo:

    st.success(
        "🎉 Congratulations! Level completed successfully."
    )

    siguiente = st.session_state.nivel_actual + 1

    if (
        siguiente in niveles
        and siguiente not in st.session_state.desbloqueados
    ):

        st.session_state.desbloqueados.append(
            siguiente
        )

        st.info(
            f"🔓 Level {siguiente} unlocked!"
        )

else:

    st.error(
        f"You need at least {minimo}% to pass this level."
    )

st.divider()

# ==========================
# DASHBOARD
# ==========================

st.subheader("📊 Student Dashboard")

niveles_completados = len(
    st.session_state.estadisticas
)

promedio = round(
    sum(
        st.session_state.estadisticas.values()
    )
    /
    len(
        st.session_state.estadisticas
    ),
    1
)

mejor = max(
    st.session_state.estadisticas.values()
)

d1, d2, d3 = st.columns(3)

d1.metric(
    "Levels Completed",
    niveles_completados
)

d2.metric(
    "Average Score",
    f"{promedio}%"
)

d3.metric(
    "Best Score",
    f"{mejor}%"
)

st.divider()

# ==========================
# CERTIFICADO FINAL
# ==========================

if len(st.session_state.desbloqueados) >= 4:

    aprobado_todo = True

    for nivel in niveles:

        if (
            nivel not in st.session_state.estadisticas
        ):
            aprobado_todo = False

    if aprobado_todo:

        st.balloons()

        st.markdown(
            """
            # 🎓 CERTIFICATE OF COMPLETION
            """
        )

        nombre = (
            st.session_state.nombre
            if st.session_state.nombre
            else "Student"
        )

        fecha = datetime.now().strftime(
            "%d/%m/%Y"
        )

        st.success(
            f"""
            This certificate is awarded to

            **{nombre}**

            for successfully completing
            all Grammar Quest levels.

            Date: {fecha}
            """
        )

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🏠 Back to Menu",
        use_container_width=True
    ):

        st.session_state.pantalla = "menu"
        st.rerun()

with col2:

    if st.button(
        "🔄 Retry Level",
        use_container_width=True
    ):

        datos = niveles[
            st.session_state.nivel_actual
        ]

        st.session_state.preguntas_actuales = (
            random.sample(
                datos["preguntas"],
                datos["cantidad"]
            )
        )

        st.session_state.indice = 0

        st.session_state.puntaje = 0

        st.session_state.respondida = False

        st.session_state.respuesta_usuario = ""

        st.session_state.inicio_pregunta = time.time()

        st.session_state.pantalla = "juego"

        st.rerun()
