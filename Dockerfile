# Verwenden Sie ein offizielles Python-Basisimage
FROM python:3.9

# Legen Sie das Arbeitsverzeichnis innerhalb des Containers fest
WORKDIR /app

# Kopieren Sie die Anwendungsabhängigkeiten in den Container
COPY requirements.txt .

# Installieren Sie die Abhängigkeiten
RUN pip install -r requirements.txt

# Kopieren Sie den Rest der Anwendung in den Container
COPY .  /app

# Setzen Sie den Befehl, um Ihre FastAPI-Anwendung auszuführen
CMD cd ./src/ ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]