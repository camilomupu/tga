from os import getenv
import re
from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema

# Cargar variables de entorno desde el archivo .env
load_dotenv('.env')

conf = ConnectionConfig(
    MAIL_USERNAME=getenv('SMTP_FROM'),
    MAIL_PASSWORD=getenv('SMTP_PASSWORD'),
    MAIL_FROM=getenv('SMTP_FROM'),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Trend Group America",
    MAIL_STARTTLS=True,  # Puedes ajustar según tus necesidades
    MAIL_SSL_TLS=False  # Puedes ajustar según tus necesidades
)

# Función para validar el formato del correo electrónico
def is_valid_email(email):
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.match(regex, email) is not None

# Función para enviar correo electrónico con resultados de la encuesta
async def send_email(email: str, resultados: dict):
    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Resultados de la Encuesta</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .container h2 {{
                    color: #ffffff;
                    background-color: #004080;
                    padding: 15px;
                    border-radius: 8px 8px 0 0;
                    text-align: center;
                }}
                .container p {{
                    color: #555555;
                    line-height: 1.6;
                }}
                .result {{
                    background-color: #e6f0ff;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    color: #777777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Resultados de la Encuesta</h2>
                <div class="result">
                    <p><strong>SNG de Satisfacción General:</strong> {resultados['sng_satisfaccion']}</p>
                    <p><strong>Total de personas que conocían a la empresa:</strong> {resultados['total_conocia_empresa']}</p>
                    <p><strong>SNG de recomendación:</strong> {resultados['sng_recomendacion']}</p>
                    <p><strong>Promedio de la recomendación:</strong> {resultados['promedio_recomendacion']}</p>
                    <p><strong>Total de personas que hicieron un comentario:</strong> {resultados['total_comentarios']}</p>
                    <p><strong>Días que llevó la encuesta:</strong> {resultados['dias_encuesta']}</p>
                    <p><strong>Meses que llevó la encuesta:</strong> {resultados['meses_encuesta']}</p>
                </div>
            </div>
            <div class="footer">
                <p>© 2020 Trend Group America | Todos los derechos reservados</p>
            </div>
        </body>
        </html>
    """
        
    message = MessageSchema(
        subject="Resultados de la Encuesta",
        recipients=[email],
        body=template,
        subtype="html"
    )
    # Enviar mensaje
    mail = FastMail(conf)
    try:
        await mail.send_message(message=message)
    except Exception:
        raise RuntimeError("Error al enviar el correo con los resultados de la encuesta")
