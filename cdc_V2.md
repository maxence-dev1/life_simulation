# Cahier des charges de la version 2

## 1. Objectif principal : 
Le but de cette V2 est d'établir une pression de l'environnement amenant à une selection plus importante. Des couts dynamiques de chaque action seront intégrés afin que la suirvie des minos dépendent majoritairement de leur attributs.


#### Modification de l'apparition de la nourriture
Désormais, la nourriture aura des zones préférentielles pour apparaitre. 

#### Modification des déplacements
- [ ] Les minos auront maintenant un mode sprint (2* la vitesse de repos mais 1.5* la consommation) et un mode repos qui sera activé selon 2 critères : 
  - [ ] si le mino à moins de 50% de sa barre de vie et qu'il voit une nourriture. 
  - [ ] Si, il a moins de 25% de sa barre de vie (mode urgence, voir plus bas)

#### Couts dynamiques
La jauge de faim devra évoluer dynamiquement, basé sur l'activité et les attributs des minos. Maintenant, chaque déplacement aura un certain prix, proportionnel à certains attributs
- [ ] Cout résistance : Les minos avec une haute résistance seront avantagés de par la taille de leur jauge mais seront désavantagé car celle- [ ]ci déscendra plus vite
- [ ] Cout Vitesse : Les minos avec une haute vitesse seront avantagés par leur vitesse de déplacement mais seront désavantagés par le cout en nourriture de se déplacer

#### Pénalités :
- [ ] Un minos qui se déplace aléatoirement consommera 25% de nourriture de plus qu'un minos qui se déplace en direction d'une nourriture
- [ ] Cout de base de la faim = Cout fixe + Vitesse * cout_vitesse + Resistance*cout_resistance (ici la vitesse indiquera donc si le mino sprint)
  
#### Mode urgence
- [ ] Mode urgence : Un minos dont sa barre de vie est inférieur à 25% de sa capacité maximum entrera en mode urgence. Un mode ou il est en sprint et ou sa vision est augmentée de 40%.

#### Mise en place d'un 'vieilissement'
- [ ] La résistance doit diminuer uniformément pour tous les minos (par exemple 0.1% toute les 100 frames)


## 3. Amélioration de l'environnement

#### Apparition de la nourriture : 
- [ ] La nourriture devra apparaitre dans certaines zones de richesses (aléatoire à terme). 70% de la nourriture devra apparaitre la dedans. 

## 4. Exigences techniques
#### Refonte de la fonction main : 
- [ ] Amélioration lisibilité code (enlever les liste de 1 éléments etc...), créer des classe SimulationConfig et SimulationEngine afin de gérer toutes les actions du main directement depuis des class

#### Adaptation de la taille des minos
La taille des minos et de la nourriture devra s'adatper au nombre de minos. (exemple : si il y a 100 minos, ils seront de taille 50, si il y en a 5000, ils seront de taille 10), idem pour la nourriture


## 5.Meilleur analyse de données : 
#### Meilleur collecte de données
Collectes de plus de données (nb de frame en aléatoire, nombre de nourriture mangées etc...) puis de les stocker dans plusieurs dataframe pour les transmettre à graph.py qui fera entierement le travail.
#### Meilleur fenetre d'analyse
Proposer une fênetre d'analyse plus modulable ou il est facile de visualiser précisement la donnée voulue. Faire une 'application' de rendu de donnée fonctionnelle


