from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime
from pymongo import DESCENDING


# conexion al servidor MongoDB

import bd
cabeceraBD = bd.cabeceraBD

# ejecutar con python -m uvicorn main:api --reload --port 8000
async def getAll():
    CabeceraDoc = cabeceraBD.find()
    return [json.loads(json_util.dumps(doc)) for doc in CabeceraDoc] if CabeceraDoc else None

async def getCabeceraPorAutor(autor : str):
    query = { "$or": [ {"de": autor}, {"para": autor} ] }
    
    # Ordenar por "fecha_hora" en orden descendente
    CabeceraDoc = list(cabeceraBD.find(query).sort("fecha_hora", DESCENDING))

    return [json.loads(json_util.dumps(doc)) for doc in CabeceraDoc] if CabeceraDoc else None

async def getCabeceraPorId(cabeceraID : ObjectId):
    cabeceraDoc = cabeceraBD.find_one({ "_id" : cabeceraID })

    return None if cabeceraDoc is None else  json.loads(json_util.dumps(cabeceraDoc))


async def crearCabecera(de: str, para: str, asunto: str):
    fecha = datetime.utcnow()
    nuevaCabecera = {
        "de": de,
        "para": para,
        "asunto": asunto,
        "stamp": fecha
    }
    
    result = cabeceraBD.insert_one(nuevaCabecera)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevaCabecera["_id"] = str(result.inserted_id)
    return nuevaCabecera
