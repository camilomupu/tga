from openai import OpenAI


client = OpenAI()

# Información del proyecto
informacion_empresa_proyecto = {
    "nombre_empresa": "Trend Group America",
    "descripcion_empresa": (
        "Somos especialistas en el conocimiento del consumidor inmobiliario"
    ),
    "descripcion_proyecto": (
        "Acompañamos a los desarrolladores inmobiliarios a través del feedback de sus clientes, de manera transversal,"
        "a lo largo de las diferentes etapas del negocio. Incorporamos este conocimiento de manera innovadora, transformándolo"
        "en una materia prima más en la toma de decisiones del negocio. Nos preocupamos de crear vínculos reales con todos los"
        "stakeholders del sector inmobiliario y constructor a través de la innovación, calidad del trabajo y fundamentos tecnológicos."
    ),
    "descripcion_enfoque": (
        "La empresa MK desarrollador inmobiliario está buscando resolver algunos problemas en su proyecto Marla, donde sus clientes"
        "realizaron muchos reclamos en la página web. Para MK el cliente es importante y estos problemas están afectando su marca."
        "Dentro de la empresa trataron de buscar una solución de forma interna, pero el personal de MK no tiene actualmente el nivel"
        "técnico y tampoco la experiencia como para llegar con un buen análisis o una solución. Responder con chatgpt algunas dudas es una cosa de ellas"
    ),
}


# Consultas
# falta ponerle el dataframe y pasarle los datos de las respuestas
def pregunta_chatGPT(pregunta: str):
    """
    Interactúa con el modelo de lenguaje GPT-3.5 Turbo de OpenAI para obtener respuestas a preguntas específicas de la app.
    Args:
        pregunta (str): Pregunta del usuario.
        db: Sesión de la base de datos.
    Returns:
        Dict[str, str]: Respuesta del modelo de lenguaje.
    """
    # Contexto del asistente
    messages = [
        {
            "role": "system",
            "content": f"Necesitamos realizar un analisis de algunas recomendaciones que nos dieron los usuarios, para ello vas a ver la respuesta que te llegue y responder dos preguntas en base a ello"
            f"a.Análisis de sentimiento. b.Problemas principales. c.Conclusion"
            f"Vas a ser un chat de una sola respuesta, 100 caracteres maximo para cada una de las respuestas"
            f"Información de la empresa y el proyecto: {informacion_empresa_proyecto}. Intenta ser un sistema solo de ayuda para Trend Group America",
        }
    ]
    # Aquí, convertimos la pregunta a minuscúlas para que sea más fácil de interpretar
    pregunta = pregunta.lower()
    # Agregamos la pregunta del usuario
    messages.append({"role": "user", "content": pregunta})

    # Hacemos la solicitud al chat
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

    response_content = response.choices[0].message.content
    return response_content
