# Mandelbrot avec Nginx

## 1. Construire et lancer les conteneurs

Depuis ce dossier :

```sh
docker compose up --build -d
```

La stack contient trois services :

- `mandelbrot` lance le serveur Python et surveille les fichiers avec un
	reloader ;
- `git-puller` partage le meme dossier et execute `git pull --ff-only` toutes
	les 30 secondes ;
- `nginx` reste le seul service expose sur `127.0.0.1:8080`.

Le dossier du depot est monte dans `mandelbrot` et `git-puller`. Quand un
nouveau commit arrive sur la branche `main`, `git-puller` le recupere, puis le
reloader redemarre le serveur Python sans reconstruire l'image.

Pour changer la branche ou la frequence de verification :

```sh
GIT_BRANCH=main PULL_INTERVAL=10 docker compose up --build -d
```

Le depot doit avoir un remote `origin` accessible depuis le conteneur. Pour un
depot prive, configure les identifiants Git dans l'environnement Docker avant
de lancer cette stack.

Le conteneur Python calcule les fractales sur le port interne `8000`.
Il n'est pas publie sur la machine. Nginx est le seul conteneur qui ouvre un
port, ici `127.0.0.1:8080`.

## 2. Afficher un resultat

Ouvrir <http://localhost:8080/> dans un navigateur ou utiliser :

```sh
curl http://localhost:8080/health
curl "http://localhost:8080/mandelbrot.png?resolution=800&zoom=4&center_x=-0.75&center_y=0.1&iterations=150" -o mandelbrot.png
```

La page `http://localhost:8080/` permet de modifier les parametres depuis le navigateur :

- `resolution` : taille de l'image, entre 100 et 1200 pixels ;
- `zoom` : niveau de zoom, entre 1 et 100000 ;
- `center_x` et `center_y` : coordonnees du centre de la vue ;
- `iterations` : precision du calcul, entre 20 et 500.

Le resultat est volontairement en noir et blanc : l'ensemble de Mandelbrot est
noir et l'arriere-plan est blanc.

## 3. Arreter

```sh
docker compose down
```