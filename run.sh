# Création d'un image Docker
#docker build . -t ynov-api

# Démarrer un conaitner docker
docker run -p 8000:4242 -e PORT=4242 -v "$(pwd):/home/app" -it ynov-api