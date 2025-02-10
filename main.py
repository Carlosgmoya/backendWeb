from services import cabecera as cabeceraAPI
from services import cuerpo as cuerpoAPI
from services import mensaje as mensajeAPI
from services import imagenes as imagenes

from fastapi import FastAPI, Request, HTTPException, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from bson.objectid import ObjectId
import shutil
import os
from pathlib import Path



app = FastAPI()
# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a la URL de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# prefijo para todas las URLs
path = "/parcial"

# Desde el directorio de este archivo: 2 maneras de ejecutar el modulo:
#   -ejecutar de manera local -> python -m uvicorn main:api --reload --port 8001

@app.get("/")
async def root():
    return {"message": "API funcionando en la nube!"}


@app.get(path + "/cabecera/{autor}")
async def getCabecera(autor: str):
    return await cabeceraAPI.getCabeceraPorAutor(autor)

@app.get(path + "/mensaje/{cabeceraID}")
async def getMensaje(cabeceraID: str):
    try:
        ObjID = ObjectId(cabeceraID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    mensaje = await mensajeAPI.getMensajeCabecera(ObjID)


    cuerpo_id = mensaje.get("cuerpo", {}).get("$oid")
    cuerpo_obj = ObjectId(cuerpo_id)
    cuerpo = await cuerpoAPI.getCuerpoPorId(cuerpo_obj)
    cabecera = await cabeceraAPI.getCabeceraPorId(ObjID)

    return {"cabecera": cuerpo, "cuerpo": cabecera}


@app.post(path + "/mensaje")
async def crearMensaje(de: str = Form(...), para: str = Form(...), asunto: str = Form(...), contenido: str = Form(...), imagen: UploadFile = File(...)):
    carpeta_destino = Path("imagenes_temporales")
    carpeta_destino.mkdir(parents=True, exist_ok=True)
    rutaLocal = carpeta_destino / imagen.filename
    with rutaLocal.open("wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    if rutaLocal:  # Si el usuario seleccionó un archivo
        rutaRemota = f"/{imagen.filename}"  # Asignar un nombre de archivo en Dropbox
        imagenes.subirImagenDropbox(rutaLocal, rutaRemota)
        enlace = imagenes.obtenerEnlaceImagen(rutaRemota)
    else:
        print("No se seleccionó ningún archivo.")
    os.remove(rutaLocal)
    cabecera = await cabeceraAPI.crearCabecera(de, para, asunto)
    cuerpo = await cuerpoAPI.crearCuerpo(contenido, enlace, "token")

    return await mensajeAPI.crearMensaje(cabecera["_id"], cuerpo["_id"])

'''
@app.get(path + "/pelis/{nombre}")
async def getPelicula(nombre: str):
    peliculaJSON = await peliculasAPI.getPeli(nombre)
    if peliculaJSON is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrado")
    
    return peliculaJSON
    
    
@app.post(path + "/pelis")
async def crearPelicula(titulo: str = Form(...), imagen: UploadFile = File(...)):
    peliculasJSON = await peliculasAPI.getPeli(titulo)
    carpeta_destino = Path("imagenes_temporales")
    carpeta_destino.mkdir(parents=True, exist_ok=True)
    rutaLocal = carpeta_destino / imagen.filename
    with rutaLocal.open("wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    if rutaLocal:  # Si el usuario seleccionó un archivo
        rutaRemota = f"/{imagen.filename}"  # Asignar un nombre de archivo en Dropbox
        imagenes.subirImagenDropbox(rutaLocal, rutaRemota)
        enlace = imagenes.obtenerEnlaceImagen(rutaRemota)
    else:
        print("No se seleccionó ningún archivo.")
    os.remove(rutaLocal)

    return await peliculasAPI.crearPeli(titulo, enlace) if peliculasJSON is None else "Ya existe una Pelicula con ese nombre"



@app.put(path + "/pelis/{pelisID}")
async def actualizarPelicula(request: Request, pelisID: str):
    try:
        ObjID = ObjectId(pelisID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    

    data = await request.json()
    titulo = data.get("titulo")
    imagen = data.get("imagen")
    
    result = await peliculasAPI.actualizarPeli(ObjID, titulo, imagen)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    if result.modified_count == 0:
        return "No se realizaron cambios"
    
    return "Pelicula actualizada con éxito"

@app.delete(path + "/pelis/{pelisID}")
async def eliminarPelicula(pelisID: str):
    try:
        obj_id = ObjectId(pelisID)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    result = await peliculasAPI.eliminarPeli(obj_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")

    return "Pelicula eliminada con éxito"

@app.get(path + "/salas")
async def getAllSalas():
    return await cabeceraAPI.getTodasSalas()



@app.get(path + "/salas/{nombre}")
async def getSala(nombre: str):
    salaJSON = await cabeceraAPI.getSala(nombre)
    if salaJSON is None:
        raise HTTPException(status_code=404, detail="Sala no encontrado")
    
    return salaJSON
    
    
@app.post("/parcial/salas")
async def crearSala(request: Request):
    data = await request.json()  # Recibir JSON del frontend
    nombre = data.get("nombre")
    propietario = data.get("propietario")  # Email del usuario autenticado
    coordenadas = data.get("coordenadas")

    if not nombre or not propietario or not coordenadas:
        return {"error": "Faltan datos"}

    salaJSON = await cabeceraAPI.getSala(nombre)

    if salaJSON is None:
        return await cabeceraAPI.crearSala(nombre, propietario, coordenadas)
    else:
        return {"error": "Ya existe una sala con ese nombre"}

@app.put(path + "/salas/{salasID}")
async def actualizarSala(request: Request, salasID: str):
    try:
        ObjID = ObjectId(salasID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    

    data = await request.json()
    nombre = data.get("nombre")
    propietario = data.get("propietario")
    coordenadas = data.get("coordenadas")
    
    result = await cabeceraAPI.actualizarSala(ObjID, nombre, propietario, coordenadas)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    if result.modified_count == 0:
        return "No se realizaron cambios"
    
    return "Sala actualizada con éxito"


@app.delete(path + "/salas/{salaID}")
async def eliminarSala(salaID: str):
    try:
        obj_id = ObjectId(salaID)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    result = await cabeceraAPI.eliminarSala(obj_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sala no encontrada")

    return "Sala eliminada con éxito"
    '''