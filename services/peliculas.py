from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime


# conexion al servidor MongoDB

import bd
peliculasBD = bd.peliculasBD

# ejecutar con python -m uvicorn main:api --reload --port 8000

async def getPeli(titulo : str):
    PeliDoc = peliculasBD.find_one({ "titulo" : titulo })

    return None if PeliDoc is None else json.loads(json_util.dumps(PeliDoc))

async def getPeliID(titulo : str):
    PeliDoc = peliculasBD.find_one({ "titulo" : titulo })

    return None if PeliDoc is None else str(PeliDoc["_id"])

async def getTodasPeliculas():
    peliDoc = peliculasBD.find().sort({"titulo":1})
    peliJSON = [json.loads(json_util.dumps(doc)) for doc in peliDoc]    # collection.find() retrieves documents in BSON format from MongoDB.
                                                                            # json_util.dumps(doc) converts BSON documents, including ObjectId fields, to JSON strings.
                                                                            # json.loads(...) transforms each document back into a Python dictionary, so it’s compatible with FastAPI's JSON response model.
    return peliJSON

async def crearPeli(titulo: str, imagen: str):
    nuevaPeli = {
        "titulo": titulo,
        "imagen": imagen,
    }
    
    result = peliculasBD.insert_one(nuevaPeli)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevaPeli["_id"] = str(result.inserted_id)
    return nuevaPeli

async def actualizarPeli(peliID: ObjectId, titulo: str, imagen: str,):
    result = peliculasBD.update_one({"_id": peliID},
                                {"$set":
                                 {"titulo": titulo,
                                 "imagen": imagen}
                                })
    return result


async def eliminarPeli(PeliID: ObjectId):
    
    result = peliculasBD.delete_one({"_id": PeliID})

    return result