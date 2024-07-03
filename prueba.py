import streamlit as st
import asyncio
from config.database import obtener_datos
from controllers.consultas import *
from config.correo import *
from controllers.streamlit_help import *
from config.chat import pregunta_chatGPT

# Configuración de la página
st.set_page_config(
    page_title="PruebaTGA",
    page_icon="💻",
)

st.sidebar.success("Consulta tus datos!")

# Título y descripción principal
st.markdown(
    "<h1 style='text-align: center;'>Prueba Desarrollador Backend</h1>",
    unsafe_allow_html=True,
)

# Mostrar imagen
img = "https://www.trendgroupamerica.com/wp-content/uploads/2020/03/logo-tga_w_1.png"
# Centro y redimensiono la imagen usando HTML y CSS
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="{img}" width="400">
    </div>
    """,
    unsafe_allow_html=True,
)

# Descripción de la empresa
st.write(
    """
Bienvenidos a nuestra plataforma de visualización de datos, diseñada para transformar
la manera en que los desarrolladores inmobiliarios comprenden y utilizan la información 
de sus clientes. Utilizando Streamlit, hemos creado una herramienta intuitiva y poderosa 
que permite visualizar los resultados de las encuestas realizadas, con el soporte de Pandas
para el manejo y análisis de datos.

En este espacio, podrán explorar de manera interactiva los datos recogidos, obteniendo insights
valiosos para mejorar la satisfacción del cliente y optimizar los proyectos inmobiliarios. 
A través de tablas y gráficos generados dinámicamente, nuestra plataforma facilita la toma de 
decisiones basada en datos capturados en tiempo real y cuando se requieran, asegurando una mejor 
comprensión y respuesta a las necesidades de los clientes.
"""
)

# Inicializar estados de sesión
if "consultas_realizadas" not in st.session_state:
    st.session_state.consultas_realizadas = False
if "email_enviado" not in st.session_state:
    st.session_state.email_enviado = False
if "resultados" not in st.session_state:
    st.session_state.resultados = {}
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "recomendaciones" not in st.session_state:
    st.session_state.recomendaciones = []

# Botón para realizar las consultas
if st.button("Realizar Consultas"):
    df = obtener_datos()
    # Primera consulta, SNG de la pregunta satisfecha general
    sng_satisfaccion = calcular_sng(df, "satisfeccion_general")
    # Segunda consulta, Total de personas que respondieron que conocían a la empresa
    total_conocia_empresa = contar_respuestas_si(df)
    # Tercera consulta, SNG de la recomendación
    sng_recomendacion = calcular_sng(df, "recomendacion")
    # Cuarta consulta, nota promedio de la recomendación
    promedio_recomendacion = calcular_promedio_recomendacion(df)
    # Quinta consulta, total de personas que hicieron un comentario
    total_comentarios = contar_comentarios(df)
    # Sexta consulta, días, meses que llevo la encuesta
    tiempo_encuesta = calcular_tiempo_encuesta(df)
    # Séptima consulta, obtener recomendaciones abiertas no nulas
    recomendaciones_abiertas = df[df["recomendacion_abierta"].notnull()]["recomendacion_abierta"].tolist()

    # Guardar resultados en el estado de sesión
    st.session_state.resultados = {
        "sng_satisfaccion": sng_satisfaccion,
        "total_conocia_empresa": total_conocia_empresa,
        "sng_recomendacion": sng_recomendacion,
        "promedio_recomendacion": promedio_recomendacion,
        "total_comentarios": total_comentarios,
        "dias_encuesta": tiempo_encuesta[0],
        "meses_encuesta": tiempo_encuesta[1],
    }
    st.session_state.consultas_realizadas = True
    st.session_state.recomendaciones = recomendaciones_abiertas

# Mostrar resultados almacenados en el estado de sesión si ya se han realizado las consultas
if st.session_state.consultas_realizadas:
    mostrar_resultados()

    # Selección de opción para enviar los resultados
    opcion = st.selectbox(
        "Seleccione una opción para enviar los resultados:",
        ("Selecciona una opción", "Enviar por correo", "Descargar PDF"),
    )

    if opcion == "Enviar por correo":
        email = st.text_input(
            "Ingresa tu correo electrónico para recibir los resultados:"
        )

        if st.button("Enviar correo"):
            if is_valid_email(email):
                st.spinner("Enviando resultados al correo...")
                asyncio.run(send_email(email, st.session_state.resultados))
                st.success("Resultados enviados exitosamente al correo proporcionado.")
                st.session_state.email_enviado = True
            else:
                st.error("Por favor, ingresa un correo electrónico válido.")

    elif opcion == "Descargar PDF":
        pdf_buffer = generar_pdf(st.session_state.resultados)
        st.download_button(
            label="Descargar PDF",
            data=pdf_buffer,
            file_name="resultados_encuesta.pdf",
            mime="application/pdf",
        )

# Sección de análisis de recomendaciones abiertas
st.markdown("### Análisis de Recomendaciones Abiertas")

if st.session_state.recomendaciones:
    index = st.session_state.current_index
    recomendacion_actual = st.session_state.recomendaciones[index]
    
    st.write(f"**Recomendación {index + 1}:** {recomendacion_actual}")

    if st.button("Analizar Recomendación"):
        with st.spinner("Analizando la recomendación..."):
            resultado = pregunta_chatGPT(recomendacion_actual)
            st.write(f"**{resultado.split('a. ')[1].split('b.')[0].strip()}**")
            st.write(f"**{resultado.split('b. ')[1].split('c.')[0].strip()}**")
            st.write(f"**{resultado.split('c. ')[1].strip()}**")

    col1, col2, _ = st.columns([1, 1, 2])
    if col1.button("Anterior", disabled=index == 0):
        st.session_state.current_index -= 1
    if col2.button("Siguiente", disabled=index == len(st.session_state.recomendaciones) - 1):
        st.session_state.current_index += 1
else:
    st.write("No hay recomendaciones abiertas para analizar, consulta los datos.")

# Sección de contacto
st.markdown("### ¿Tienes alguna pregunta?")
st.write(
    "Desarrollado por Daniel Muñoz Puentes. [Contacto](mailto:danielcamilomu35@gmail.com)"
)