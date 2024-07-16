# Image de base officielle Python
FROM python:3.9

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie du fichier requirements.txt dans le répertoire de travail
COPY requirements.txt /app/

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Clonage du contenu de l'application dans le répertoire de travail
COPY . /app/

# Exposition du port sur lequel Django s'exécute
EXPOSE 8000

# Lancement du server de l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
