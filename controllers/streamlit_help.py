from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
import streamlit as st


# Función para mostrar resultados
def mostrar_resultados():
    st.write(
        "SNG de Satisfacción General:", st.session_state.resultados["sng_satisfaccion"]
    )
    st.write(
        "Total de personas que conocían a la empresa:",
        st.session_state.resultados["total_conocia_empresa"],
    )
    st.write("SNG de recomendación:", st.session_state.resultados["sng_recomendacion"])
    st.write(
        "Promedio de la recomendacion:",
        st.session_state.resultados["promedio_recomendacion"],
    )
    st.write(
        "Total de personas que hicieron un comentario:",
        st.session_state.resultados["total_comentarios"],
    )
    st.write(
        f"Días que llevó la encuesta:", st.session_state.resultados["dias_encuesta"]
    )
    st.write(
        f"Meses que llevó la encuesta:", st.session_state.resultados["meses_encuesta"]
    )


# Función mejorada para generar PDF
def generar_pdf(resultados):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    # Estilos de párrafo y tabla
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = styles["Normal"]
    # Título del PDF
    title = Paragraph("Resultados de la Encuesta", title_style)
    elements.append(title)
    elements.append(Paragraph("<br/>", normal_style))  # Agregar un espacio
    # Datos para la tabla
    data = [
        ["Descripción", "Resultado"],
        ["SNG de Satisfacción General", resultados["sng_satisfaccion"]],
        [
            "Total de personas que conocían a la empresa",
            resultados["total_conocia_empresa"],
        ],
        ["SNG de recomendación", resultados["sng_recomendacion"]],
        ["Promedio de la recomendacion", resultados["promedio_recomendacion"]],
        [
            "Total de personas que hicieron un comentario",
            resultados["total_comentarios"],
        ],
        ["Días que llevó la encuesta", resultados["dias_encuesta"]],
        ["Meses que llevó la encuesta", resultados["meses_encuesta"]],
    ]
    # Crear tabla
    table = Table(data)
    # Estilo de la tabla
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(style)
    # Añadir tabla a los elementos del PDF
    elements.append(table)
    # Construir el PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
