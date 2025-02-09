import dropbox
import requests

APP_KEY = '0c29rx6w768ojzo'
APP_SECRET = 'gxivjm137sw08gq'
REFRESH_TOKEN = 'OAvdI__SeIcAAAAAAAAAAe4eUjcDs5kscwNgD_cqdFpLqMW_oMH0it2PGCMJmYy2'


def renovar_access_token():
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": APP_KEY,
        "client_secret": APP_SECRET,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print(f"Nuevo Access Token: {access_token}")
        return access_token
    else:
        print(f"Error al renovar el token: {response.json()}")
        return None
ACCESS_TOKEN = renovar_access_token()
if ACCESS_TOKEN:
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
else:
    print("No se pudo obtener un Access Token válido.")
    dbx = None

def verificarYRenovarToken():
    """Verifica si el token está válido y lo renueva si es necesario."""
    global dbx
    try:
        # Intentamos realizar una operación simple para verificar el token
        dbx.users_get_current_account()
    except dropbox.exceptions.AuthError:
        print("El token de acceso ha caducado. Renovando...")
        ACCESS_TOKEN = renovar_access_token()
        dbx = dropbox.Dropbox(ACCESS_TOKEN)

def generarNombreUnico(ruta_remota):
    """Genera un nombre único si el archivo ya existe en Dropbox."""
    try:
        # Si el archivo ya existe, generamos un nuevo nombre
        dbx.files_get_metadata(ruta_remota)
        ruta, nombre_archivo = ruta_remota.rsplit('/', 1) if '/' in ruta_remota else ('', ruta_remota)
        nombre, extension = nombre_archivo.rsplit('.', 1) if '.' in nombre_archivo else (nombre_archivo, '')
        contador = 1

        while True:
            nuevo_nombre = f"{nombre} ({contador})"
            if extension:
                nuevo_nombre += f".{extension}"
            nuevo_ruta_remota = f"{ruta}/{nuevo_nombre}" if ruta else f"/{nuevo_nombre}"
            nuevo_ruta_remota = nuevo_ruta_remota.replace('//', '/')  # Normaliza la ruta
            try:
                dbx.files_get_metadata(nuevo_ruta_remota)
            except dropbox.exceptions.ApiError:
                # Si no existe, devolvemos el nuevo nombre
                return nuevo_ruta_remota
            contador += 1
    except dropbox.exceptions.ApiError:
        # Si no existe, devolvemos el nombre original
        return ruta_remota


def subirImagenDropbox(rutaLocal, rutaRemota):
    verificarYRenovarToken()
    try :
        rutaRemota = generarNombreUnico(rutaRemota)
        with open(rutaLocal, 'rb') as archivo:
            dbx.files_upload(archivo.read(), rutaRemota, mode=dropbox.files.WriteMode.add)
            print(f"Imagen subida a {rutaRemota}")
    except FileNotFoundError:
        print("Archivo no encontrado. Asegúrate de seleccionar un archivo.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")


def obtenerEnlaceImagen(rutaRemota):
    try:
        # Intenta recuperar un enlace compartido existente
        enlaces_existentes = dbx.sharing_list_shared_links(path=rutaRemota).links
        if enlaces_existentes:
            enlaceCompartido = enlaces_existentes[0].url
        else:
            # Si no hay enlaces existentes, crea uno nuevo
            enlaceCompartido = dbx.sharing_create_shared_link_with_settings(rutaRemota).url
        
        # Modificar el enlace para que sea un enlace directo (descarga)
        if '?dl=0' in enlaceCompartido:
            enlaceDescarga = enlaceCompartido.replace('?dl=0', '?raw=1')
        else:
            enlaceDescarga = f"{enlaceCompartido}&raw=1"
        return enlaceDescarga
    except dropbox.exceptions.ApiError as e:
        print(f"Error al obtener el enlace: {e}")
        return None