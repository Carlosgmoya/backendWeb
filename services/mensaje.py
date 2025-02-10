from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime
from pymongo import DESCENDING
from fastapi.responses import JSONResponse

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
    from fastapi.encoders import jsonable_encoder

async def crearMensaje(cabecera: ObjectId, cuerpo: ObjectId):
    nuevoMensaje = {
        "cabecera": str(cabecera),  # Convertir ObjectId a str
        "cuerpo": str(cuerpo)       # Convertir ObjectId a str
    }
    
    result = mensajeBD.insert_one(nuevoMensaje)
    nuevoMensaje["_id"] = str(result.inserted_id)  # Asegúrate de que el _id también sea un str
    
    return JSONResponse(content=nuevoMensaje)