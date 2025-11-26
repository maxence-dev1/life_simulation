# Life simulation 

## Objectif global


Le projet sera une application où il sera possible de simuler la vie de x objets. Le monde suivra des règles instaurées à l'avance. 
Chaque objet aura plusieurs attributs (alignés selon certaines normes) mais tous différents. A la fin de la génération, les données récupérées seront stockées dans un fichier csv et analysables. 
Il y aura plusieurs version, chaque version sera meilleure et plus poussée que la précédente.
L'objectif de ce projet va être de pouvoir acquérir et mettre en oeuvre plusieurs compétences. 
- Architecture globale d'un projet
- Développement logiciel  
- POO
- Optimisation 
- Récupération des données
- Netoyage et interfaçage
- Analyse et manipulation en python

## Version 1 :

Cette première version implémentera le fonctionnement primaire des objets que l'on appelera des Minos.
Ces Minos auront pour seul but de survivre. Pour survivre, un Mino doit garder se nourir et garder sa jauge de nourriture au dessus d'un certain seuil. Cette nouriture apparaitra aléatoirement sur la map à des intervalles aléatoires. Premier arrivé, premier servi. La jauge de faim commence à 100 (fois le multiplicateur resistance) et baisse de 0.1 par frame (un mino à environ 1000 frame avant de mourir de faim).
Chaque mino est indentifié avec un id unique qui est son indice dans la liste les contenant
Les Minos auront plusieurs attributs, tous noté sur __. A leur naissance (début de la simulation), ils auront X points de compétence à partager entre ces attributs. Ces attributs seront éparpillés autour d'une moyenne définie suivant une loi gautienne (les meilleurs ou les plus nuls sont les plus rare) : 
- Champ de vision : savoir à quel distance il detecte de la nourriture. 
- Résistance à la faim : Loi gaussienne centrée en 1, de variance 0.6 (taille de la jauge maximale)
- Vitesse : Loi gaussienne centrée en 5, de variance 0.6
- Satiété (quantité bonus ou malus que donne la nouriture)

### Déplacement des Mino :
Chacun selectionne un point sur l'écran et essaie de s'y rendre. Quand il y est il en choisi un nouveau.

### Utilisation : 
L'utilisateur aura un interface où il choisira les paramètres de sa simulation (nombre de minos, esperence de la vitesse...). Il aura ensuite accès à la simulation ou il pourra accelerer le temps (verifier qu'on reste à un certain fps), il y aura ensuite les graphiques disponibles.

### Liste des données récoltées
Les données seront enregistrées tout au long de la simulation, elles sont ensuites envoyées vers graph.py pour les graphiques.
- évolution de la jauge de faim de chaque mino

### Affichage des données
Les données seront affichées via le fichier graph qui utilise la bibli matplotlib

Pour le moment c'est assez rudimentaire mais cela devrait suffire à étudier un échantillon. 
