# OCR_Projet_2
## Description
Il s'agit du projet numéro 2 du parcours *Développeur d'application Python* d'OpenClassrooms
## Environnement virtuel
Commencez par télécharger [Python](https://www.python.org/downloads) si vous ne l'avez pas déjà!\
**Créez un environnement virtuel** dans lequel vous allez **placer le script ScrappingV2.py**.
#### Si vous n'avez pas virtualenv, installez-le à partir d'un terminal :

```shell
pip install virtualenv
```
![install_virtualenv](https://puu.sh/I2oHu/f607c41fcb.png)

#### Placez-vous dans le dossier que vous souhaitez puis créez l'environnement virtuel comme ceci:
```shell
py -m virtualenv venv
```
![création_virtualenv](https://puu.sh/I2oMZ/dd5c49de3f.png)

#### Activez maintenant l'environnement virtuel :
```shell
venv\Scripts\activate
```
![activate](https://puu.sh/I2oQd/d1b5620bbf.png)

#### Il faut maintenant installer requests :
```shell
pip install requests
```
![requests](https://puu.sh/I2oRd/a764c22b45.png)

Vous êtes prêt à utiliser le script!

## Usage
Une fois l'environnement virtuel **installé et activé**, exécutez le script comme ceci:
```shell
ScrappingV2.py
```

Il n'y a qu'une input, il s'agit des index des catégories que vous désirez scraper.\
La syntaxe à utiliser est la suivante:
```python
Une seule catégorie -> index
Plusieurs catégories -> index:index
```
L'**INDEX** doit être un **NOMBRE** entre **0** et **52**.\
Pour **scraper le site entier** il faudra écrire **0:52**.

## Exemples

![Exemple](https://puu.sh/I2oS0/f926e7ce96.png)

## Requirements
N'ayant utilisé aucune librairie externe le fichier requirement.txt est vide.

## Branche BeautifulSoup
Il s'agit de la première version du projet où j'ai utilisé la librairie Beautifulsoup. Cette version est obsolète !
