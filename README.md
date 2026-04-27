# 🌤️ App del Tiempo

Una aplicación web sencilla hecha con **Python** y **Flask** que muestra el tiempo actual de cualquier ciudad del mundo usando la API de OpenWeatherMap.

---

## 📸 ¿Qué hace?

- Busca el tiempo de cualquier ciudad
- Muestra temperatura, descripción, humedad y viento

---

## ⚙️ Requisitos

- Python 3.x instalado → [python.org](https://www.python.org/downloads/)
- Una API key gratuita de OpenWeatherMap → [openweathermap.org](https://openweathermap.org/)

---

## 🚀 Cómo ejecutarlo

### 1. Clona o descarga el repositorio

```bash
git clone https://github.com/TU_USUARIO/app-del-tiempo.git
cd app-del-tiempo
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 3. Añade tu API key

Abre el archivo `app.py` y sustituye `INSERTA_TU_API_KEY_AQUI` por tu clave de OpenWeatherMap:

```python
API_KEY = "INSERTA_TU_API_KEY_AQUI"
```

### 4. Ejecuta la app

```bash
python app.py
```

> En Windows, si `python` no funciona, usa `py app.py`

### 5. Abre el navegador

Ve a: [http://127.0.0.1:8080](http://127.0.0.1:5000) o [http://localhost:8080](http://localhost:8080)

---

## 📁 Estructura del proyecto

```
App-del-Tiempo/
├── app.py              # Servidor Flask principal
├── requirements.txt    # Dependencias del proyecto
└── templates/
    └── index.html      # Interfaz de usuario
```

---

## 🛠️ Tecnologías usadas

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [OpenWeatherMap API](https://openweathermap.org/api)

---

## 📝 Licencia

Proyecto de uso libre para aprendizaje y portfolio.
