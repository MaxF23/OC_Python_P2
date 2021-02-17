# OC_Python_P2
# Utilisez les bases de Python pour l'analyse de marché*

### Installation

- Télécharger et placer les fichiers dans le répertoire voulu

- Ouvrir le terminal et se placer dans le répertoire précédemment choisi grâce à la commande 
  ```
  cd chemin/vers/répertoire
  ```

  - Optionnel : vérifier si les fichiers _requirements.txt_ et _scraper.py_ s'affichent lorsque l'on rentre la commande 
    ```
    ls
    ```
  

- Créer un environnement virtuel python grâce à la commande 
  ```
  python -m venv nomdelenvironnement
  ```

- Activer l’environnement virtuel grâce à la commande 
  ```
  source nomdelenvironnement/bin/activate
  ```

- Installer les modules nécessaires à l’utilisation du programme grâce à la commande 
  ```
  pip install -r requirements.txt
  ```

### Execution

- Executer le programme 
  ```
  python scraper.py
  ```

- Après son execution (qui dure quelques minutes) le programme va créer dans le répertoire courant un fichier _Images_ contenant toutes les images des livres présents sur Book to scrape en format .jpg classées dans des fichiers differents pour chaque catégories et un fichier _CSV_ contenant, par catégories, toutes les informations sur les livres en format CSV 

