import pandas as pd
from unicodedata import normalize


# Primera consulta, SNG de la pregunta satisfeccion_general
def calcular_sng(df, columna: str):
    total_respuestas = len(df[columna])
    satisfaccion = len(df[(df[columna] == 6) | (df[columna] == 7)])
    insatisfaccion = len(df[(df[columna] >= 1) & (df[columna] <= 4)])
    sng = round((satisfaccion * 100) / total_respuestas) - round(
        (insatisfaccion * 100) / total_respuestas
    )
    return sng


# Segunda consulta, Total de personas que respondieron que conocían a la empresa
def contar_respuestas_si(df):
    df["conocia_empresa"] = (
        df["conocia_empresa"]
        .str.lower()
        .apply(lambda x: normalize("NFKD", x).encode("ASCII", "ignore").decode("ASCII"))
    )
    total_si = len(df[df["conocia_empresa"].str.contains("si")])
    return total_si


# Cuarta consulta, nota promedio de la recomendación
def calcular_promedio_recomendacion(df):
    promedio_recomendacion = round(df["recomendacion"].mean(), 2)
    return promedio_recomendacion


# Quinta consulta, total de personas que hicieron un comentario
def contar_comentarios(df):
    total_comentarios = df["recomendacion_abierta"].notna().sum()
    return total_comentarios


# Sexta consulta, días, meses que llevo la encuesta
def calcular_tiempo_encuesta(df):
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d %H:%M:%S")
    fecha_inicio = df["fecha"].min()
    fecha_fin = df["fecha"].max()
    dias_encuesta = (fecha_fin - fecha_inicio).days
    meses_encuesta = (
        (fecha_fin.year - fecha_inicio.year) * 12 + fecha_fin.month - fecha_inicio.month
    )
    return (dias_encuesta, meses_encuesta)
