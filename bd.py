from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://carlos:1234@cluster0.bv6um.mongodb.net/retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Wiki conectado a MongoDB!")
except Exception as e:
    print(e)

# Base de Datos

database = client["Final2425"]

peliculasBD = database["Peliculas"]
salasBD = database["Salas"]
proyeccionesBD = database["Proyecciones"]