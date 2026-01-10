Un **minos** est une entité biologique simple dont l'objectif unique est la survie. Pour ne pas mourir, il doit constamment maintenir sa jauge de nourriture au dessus de 0.

## Attributs et génétique
Chaque minos possède 4 attributs définis à la naissance selon une **loi Normale**. Ces attributs sont fixés et impactent directement la consommation d'énergie.

| Attribut         | Description                                                       | Impact Énergétique |
| :--------------- | :---------------------------------------------------------------- | :----------------- |
| **Résistance**   | Capacité maximale de la jauge de nourriture.                      | Moyen              |
| **Vitesse**      | Rapidité de déplacement sur la carte.                             | Très Élevé         |
| **Assimilation** | Efficacité nutritive (quantité de nourriture gagnée en mangeant). | Nul                |
| **Vision**       | Rayon de détection de la nourriture.                              | Faible             |


Comme dans la vraie vie, chaque attribut à un **coût** qui est ici représenté par une dépense d'énergie plus importante

## Cycle de vie



### **Naissance** :  le Minos apparait aléatoirement sur la carte
- **Jauge initiale** : 100 unités + 25% de sa capacité max
- **Génétique** : Les attributs sont tirés au sort (Loi Normale), créant une population variée avec des individus moyen et quelques exeptions. 


### **Vie et comportement** : à chaque instant, le Minos analyse son environnement
1. **Zone d'abondance** : S'il en détecte une, il s'y dirige immédiatement
2. **Recherche active** : Sinon, il choisi la nourriture la plus proche
3. **Errance** : si aucune nourriture n'est visible, il se dirige vers un point aléatoire. Cela augmentera sa consommation

!!! info "Alimentation"
    Lorsque le Minos entre en collision avec une nourriture, sa jauge de nourriture augmente en suivant la formule : 
    
    $$J = J + V_{aleur_nourriture}+15 \times S_{atiété}$$




### **Mode urgence (sprint)** : si la jauge de nourriture descend en dessous des 50% et qu'une nourriture est visible : 
- La bordure du Minos devient jaune
- Sa vitese est doublé
- Sa consommation d'énergie augmente drastiquement

### **Mort** : Lorsque la jauge de nourriture atteind 0, le Minos meurt. Il devient noir avant de disparaitre.

!!! info "Modèle de consommation énergétique"
    La consommation d'un Minos est calculé à chaque frame. Ce modèle garantit un équilibre entre les capacités physique et la survie.

    **Formule :**
    
    $$C = 0.5 + (R_{esistance} \times 0.1) + (V_{ision} \times 0.001) + (V_{itesse}^{1.3} \times R \times 0.005) + M$$

    **Détails des variables :**
    * **$M$** : Malus de recherche ($0.25$) si aucune cible n'est identifiée, $0$ sinon.



### Indicateurs Visuels : 
- **Couleur du corps** : Varie du **vert** (rassasié) au **rouge** (Affamé)
- **Contour** :  Passe au **jaune** lorsque le Minos sprint
- **Corps noir** : Minos mort
