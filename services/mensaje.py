from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime
from pymongo import DESCENDING


# conexion al servidor MongoDB

import bd
mensajeBD = bd.mensajeBD

# ejecutar con python -m uvicorn main:api --reload --port 8000

async def getMensaje(mensajeId: ObjectId):
    mensajeDoc = mensajeBD.find_one({ "_id" : mensajeId })

    return None if mensajeDoc is None else json.loads(json_util.dumps(mensajeDoc))

async def getMensajeCabecera(cabeceraId: ObjectId):
    mensajeDoc = mensajeBD.find_one({ "cabecera" : cabeceraId })

    return None if mensajeDoc is None else json.loads(json_util.dumps(mensajeDoc))

async def crearMensaje(cabecera: ObjectId, cuerpo: ObjectId):
    nuevoMensaje = {
        "cabecera": cabecera,
        "cuerpo": cuerpo
    }
    
    result = mensajeBD.insert_one(nuevoMensaje)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevoMensaje["_id"] = str(result.inserted_id)
    return nuevoMensaje
