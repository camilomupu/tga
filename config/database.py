from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Cargar variables de entorno desde el archivo .env
load_dotenv('.env')

# Crear la URL de la base de datos
DB_URL = f'mysql+mysqlconnector://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}'

# Crear el motor de la base de datos
Engine = create_engine(DB_URL, echo=True, future=True)

def obtener_datos():
    # Leer datos de la tabla 'encuesta'
    df = pd.read_sql('SELECT * FROM encuesta', Engine)
    return df