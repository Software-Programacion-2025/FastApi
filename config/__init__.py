from dotenv import load_dotenv
import os

load_dotenv()

# Cadena de conexión a la base de datos
STRCNX=os.getenv('STRCNX')

# Configuración de la base de datos
ENGINE=os.getenv('ENGINE')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
USERDB=os.getenv('USERDB')
PASSWORD=os.getenv('PASSWORD')
DATABASE=os.getenv('DATABASE')

# STRCNX = f'{ENGINE}://{USERDB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

SQLALCHEMY_DATABSE_URI=STRCNX