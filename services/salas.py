from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime


# conexion al servidor MongoDB

import bd
salasBD = bd.salasBD

# ejecutar con python -m uvicorn main:api --reload --port 8000

async def getSala(nombre : str):
    SalaDoc = salasBD.find_one({ "nombre" : nombre })

    return None if SalaDoc is None else json.loads(json_util.dumps(SalaDoc))

async def getSalaID(nombre : str):
    SalaDoc = salasBD.find_one({ "nombre" : nombre })

    return None if SalaDoc is None else str(SalaDoc["_id"])


async def getTodasSalas():
    SalasDoc = salasBD.find().sort({"nombre":1})
    salasJSON = [json.loads(json_util.dumps(doc)) for doc in SalasDoc]    # collection.find() retrieves documents in BSON format from MongoDB.
                                                                            # json_util.dumps(doc) converts BSON documents, including ObjectId fields, to JSON strings.
                                                                            # json.loads(...) transforms each document back into a Python dictionary, so it’s compatible with FastAPI's JSON response model.
    return salasJSON

async def crearSala(nombre: str, propietario: str, coordenadas: list[float]):
    nuevaSala = {
        "nombre": nombre,
        "propietario": propietario,
        "coordenadas": coordenadas
    }
    
    result = salasBD.insert_one(nuevaSala)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevaSala["_id"] = str(result.inserted_id)
    return nuevaSala

async def actualizarSala(salaID: ObjectId, nombre: str, propietario: str, coordenadas: list[float] ):
    result = salasBD.update_one({"_id": salaID},
                                {"$set":
                                 {"nombre": nombre,
                                 "propietario": propietario,
                                 "coordenadas": coordenadas}
                                })
    return result


async def eliminarSala(SalaID: ObjectId):
    
    result = salasBD.delete_one({"_id": SalaID})

    return result