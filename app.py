from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "INSERTA_TU_API_KEY_AQUI"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

def obtener_condicion(weather_main):
    condiciones = {
        "Clear": "clear",
        "Clouds": "clouds",
        "Rain": "rain",
        "Drizzle": "drizzle",
        "Thunderstorm": "thunderstorm",
        "Snow": "snow",
        "Mist": "mist",
        "Fog": "fog",
        "Haze": "haze",
    }
    return condiciones.get(weather_main, "default")

def formatear_hora(timestamp, timezone_offset):
    from datetime import timezone, timedelta
    tz = timezone(timedelta(seconds=timezone_offset))
    return datetime.fromtimestamp(timestamp, tz=tz).strftime("%H:%M")

def obtener_prevision_5dias(lat, lon):
    respuesta = requests.get(FORECAST_URL, params={
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "es"
    })
    if respuesta.status_code != 200:
        return []

    datos = respuesta.json()
    dias = {}

    for item in datos["list"]:
        fecha = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
        dia_nombre = datetime.fromtimestamp(item["dt"]).strftime("%A")

        traducciones = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }
        dia_nombre = traducciones.get(dia_nombre, dia_nombre)

        if fecha not in dias:
            dias[fecha] = {
                "dia": dia_nombre,
                "fecha": datetime.fromtimestamp(item["dt"]).strftime("%d/%m"),
                "temps": [],
                "iconos": [],
                "descripciones": []
            }

        dias[fecha]["temps"].append(item["main"]["temp"])
        dias[fecha]["iconos"].append(item["weather"][0]["icon"])
        dias[fecha]["descripciones"].append(item["weather"][0]["description"])

    prevision = []
    for fecha, data in list(dias.items())[1:6]:
        prevision.append({
            "dia": data["dia"],
            "fecha": data["fecha"],
            "max": round(max(data["temps"])),
            "min": round(min(data["temps"])),
            "icono": data["iconos"][len(data["iconos"]) // 2],
            "descripcion": data["descripciones"][len(data["descripciones"]) // 2].capitalize()
        })

    return prevision

@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q", "")
    if len(query) < 2:
        return jsonify([])

    respuesta = requests.get(GEO_URL, params={
        "q": query,
        "limit": 5,
        "appid": API_KEY
    })

    if respuesta.status_code != 200:
        return jsonify([])

    resultados = []
    for lugar in respuesta.json():
        nombre = lugar.get("name", "")
        pais = lugar.get("country", "")
        estado = lugar.get("state", "")
        lat = lugar.get("lat")
        lon = lugar.get("lon")

        if estado:
            etiqueta = f"{nombre}, {estado}, {pais}"
        else:
            etiqueta = f"{nombre}, {pais}"

        resultados.append({
            "label": etiqueta,
            "value": nombre,
            "lat": lat,
            "lon": lon
        })

    return jsonify(resultados)

@app.route("/", methods=["GET", "POST"])
def index():
    tiempo = None
    prevision = []
    error = None

    if request.method == "POST":
        ciudad = request.form.get("ciudad", "")
        lat = request.form.get("lat", "")
        lon = request.form.get("lon", "")

        # Si tenemos coordenadas, buscamos por lat/lon (más preciso)
        if lat and lon:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "lang": "es"
            }
        else:
            params = {
                "q": ciudad,
                "appid": API_KEY,
                "units": "metric",
                "lang": "es"
            }

        respuesta = requests.get(BASE_URL, params=params)

        if respuesta.status_code == 200:
            datos = respuesta.json()
            lat_result = datos["coord"]["lat"]
            lon_result = datos["coord"]["lon"]
            timezone_offset = datos["timezone"]

            tiempo = {
                "ciudad": datos["name"],
                "pais": datos["sys"]["country"],
                "temperatura": round(datos["main"]["temp"]),
                "sensacion": round(datos["main"]["feels_like"]),
                "temp_max": round(datos["main"]["temp_max"]),
                "temp_min": round(datos["main"]["temp_min"]),
                "descripcion": datos["weather"][0]["description"],
                "humedad": datos["main"]["humidity"],
                "viento": datos["wind"]["speed"],
                "icono": datos["weather"][0]["icon"],
                "condicion": obtener_condicion(datos["weather"][0]["main"]),
                "presion": datos["main"]["pressure"],
                "visibilidad": round(datos.get("visibility", 0) / 1000, 1),
                "amanecer": formatear_hora(datos["sys"]["sunrise"], timezone_offset),
                "atardecer": formatear_hora(datos["sys"]["sunset"], timezone_offset),
            }

            prevision = obtener_prevision_5dias(lat_result, lon_result)

        else:
            error = "Ciudad no encontrada. Inténtalo de nuevo."

    return render_template("index.html", tiempo=tiempo, prevision=prevision, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
