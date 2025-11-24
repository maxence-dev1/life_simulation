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
Ces Minos auront pour seul but de survivre. Pour survivre, un Mino doit garder se nourir et garder sa jauge de nourriture au dessus d'un certain seuil. Cette nouriture apparaitra aléatoirement sur la map à des intervalles aléatoires. Premier arrivé, premier servi.
Les Minos auront plusieurs attributs, tous noté sur __. A leur naissance (début de la simulation), ils auront X points de compétence à partager entre ces attributs. Ces attributs seront éparpillés autour d'une moyenne définie suivant une loi gautienne (les meilleurs ou les plus nuls sont les plus rare) : 
-Résistance à la fin (taille de la jauge maximale)
-Vitesse (vitesse de déplacement)
-Satiété (quantité bonus ou malus que donne la nouriture)

Pour le moment c'est assez rudimentaire mais cela devrait suffire à étudier un échantillon. 
