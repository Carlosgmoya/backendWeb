from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime


# conexion al servidor MongoDB

import bd
proyeccionesBD = bd.proyeccionesBD

async def asignar(sala: ObjectId, pelicula: ObjectId, fechaHora):
    nuevaProyeccion = {
        "sala": sala,
        "pelicula": pelicula,
        "fechaHora": fechaHora
    }
    
    result = proyeccionesBD.insert_one(nuevaProyeccion)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevaProyeccion["_id"] = str(result.inserted_id)
    nuevaProyeccion["sala"] = str(sala)
    nuevaProyeccion["pelicula"] = str(pelicula)
    return nuevaProyeccion

async def proyeccionesPelicula(id : ObjectId):
    proyeccionesDoc =  proyeccionesBD.find({"pelicula": id})

    return [json.loads(json_util.dumps(doc)) for doc in proyeccionesDoc] 
 
async def cartelera(id : ObjectId):
    proyeccionesDoc =  proyeccionesBD.find({"sala": id})

    return [json.loads(json_util.dumps(doc)) for doc in proyeccionesDoc] 
