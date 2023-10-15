import pandas as pd
import requests
import base64

client_id = 
client_secret = 

def obtener_token_spotify(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    r = requests.post(auth_url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json().get("access_token")
    else:
        return None

def obtener_portada_spotify(token, track_name, artists_name):
    search_url = "https://api.spotify.com/v1/search"
    query = f"{track_name} {artists_name}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }
    r = requests.get(search_url, headers=headers, params=params)
    try:
        return r.json()["tracks"]["items"][0]["album"]["images"][0]["url"]
    except (KeyError, IndexError):
        print(f"No se encontró portada para: {track_name} de {artists_name}")
        return None

token = obtener_token_spotify(client_id, client_secret)
if not token:
    print("Error obteniendo el token de acceso.")
    exit()

ruta_csv = r"C:\Users\a2139\Documents\00_PERSONAL\spotify bonito\spotify-2023.csv"
df = pd.read_csv(ruta_csv, encoding="ISO-8859-1")
df['url_portada_spotify'] = df.apply(lambda x: obtener_portada_spotify(token, x['track_name'], x['artist(s)_name']), axis=1)

df.to_csv(ruta_csv, index=False)
