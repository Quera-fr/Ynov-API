# Connexion au service container d'Heroku
heroku container:login

# Création de l'application
heroku create api-ynov-kevin

# Construction de l'image Docker sous MacOS Apple Silicon
docker buildx build --platform linux/amd64 -t api-ynov-kevin .

# Construction de l'image Docker sous Windows
docker build . -t fastapi-ynov

# Tag Image Docker au registery d'Heroku
docker tag api-ynov-kevin registry.heroku.com/api-ynov-kevin/web

# Publication de l'image Docker dans le registery d'Heroku
docker push registry.heroku.com/api-ynov-kevin/web

# Configuration du cotainer
heroku stack:set container -a api-ynov-kevin

# Activation du container
heroku container:release web -a api-ynov-kevin

# Ouverture de l'application
heroku open -a api-ynov-kevin
