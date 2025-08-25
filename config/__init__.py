from dotenv import load_dotenv
import os

load_dotenv()
# Configuración de la base de datos
ENGINE=os.getenv('ENGINE')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
USERDB=os.getenv('USERDB')
PASSWORD=os.getenv('PASSWORD')
DATABASE=os.getenv('DATABASE')

# Cadena de conexión a la base de datos
ENVIROMENT = os.getenv('ENVIROMENT', 'prod')

if ENVIROMENT == 'dev':
    STRCNX=os.getenv('STRCNX')
elif ENVIROMENT == 'qa':
    STRCNX=os.getenv('STRCNXQA')
else:
    STRCNX = f'{ENGINE}://{USERDB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

SQLALCHEMY_DATABASE_URI=STRCNX