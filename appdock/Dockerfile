# Utilise une image officielle Python
FROM python:3.10

# Crée un dossier de travail dans le conteneur
WORKDIR /app

# Copie les fichiers du projet dans le conteneur
COPY . /app

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port utilisé par Streamlit
EXPOSE 8501

# Commande pour démarrer l'app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
