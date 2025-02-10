from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime


# conexion al servidor MongoDB

import bd
cuerpoBD = bd.cuerpoBD

# ejecutar con python -m uvicorn main:api --reload --port 8000

async def getCuerpoPorId(cabeceraID : ObjectId):
    cuerpoDoc = cuerpoBD.find_one({ "_id" : cabeceraID })

    return None if cuerpoDoc is None else  json.loads(json_util.dumps(cuerpoDoc))

async def getPeliID(titulo : str):
    PeliDoc = cuerpoBD.find_one({ "titulo" : titulo })

    return None if PeliDoc is None else str(PeliDoc["_id"])

async def crearCuerpo(contenido: str, adjunto: str, token: str):
    nuevoCuerpo = {
        "contenido": contenido,
        "adjunto": adjunto,
        "token": token
    }
    
    result = cuerpoBD.insert_one(nuevoCuerpo)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevoCuerpo["_id"] = str(result.inserted_id)
    return nuevoCuerpo
