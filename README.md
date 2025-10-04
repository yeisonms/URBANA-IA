# Ejemplo con PYTHON FLASK e integración de LLM mediante el API de GROQ

```
[LINUX/MAC] > python3 -m venv venv
[WINDOWS] > py.exe -m venv venv
```

Si no tiene instalado venv, Lo puede instalar de la siguiente manera:

```
[LINUX/MAC] > python3 -m pip install --user virtualenv
[WINDOWS] > py.exe -m pip install --user virtualenv
```

Una vez creado el virtual environment lo activamos para poder instalar las dependencias:

```
[LINUX/MAC] > source venv/bin/activate
[WINDOWS] > .\venv\Scripts\activate
```

Instalamos las dependencias con pip:

```
pip3 install -r requirements.txt 
```

Tenemos que crear un fichero ".env" con el contenido del token de GROQ (sustituyendo XXXXX por tu API key de https://console.groq.com/keys):
```
GROQ_API_KEY=XXXXX
```

Ejecutamos la aplicación:
```
py app.py
```

Abra un navegador y vaya a la url "http://localhost:5000" para ver la aplicación.



