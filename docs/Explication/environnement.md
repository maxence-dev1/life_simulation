# Spécifications de l'Environnement

---

## Optimisation Technique

### Système de Grille (Spatial Partitioning)
La carte est structurée selon un quadrillage précis pour garantir la fluidité de la simulation :

* **Dimensions :** Carrés de **100px × 100px**.
* **Fonction :** Les Minos limitent leur champ de recherche à leur cellule et aux cellules proches d'eux.
* **Impact :** Réduction importante des ressources utilisées.

---

### Gestion des FPS
* **Plafonnement :** La vitesse de simulation est ajustable par l'utilisateur.
* **Mode Performance :** En réglant les FPS à `-1`, la simulation s'exécute à la vitesse maximale possible.

---

### Zoom Adaptatif
L'affichage s'adapte à la densité de Minos sur la carte :

* **Échelle :** Le niveau de zoom varie selon le nombre total de Minos.
* **Rendu :** La taille visuelle des Minos et des ressources est calculée proportionnellement au zoom pour maintenir une visibilité optimale.

---

## La Zone d'Abondance

La zone d'abondance est un rectangle dynamique conçu pour stimuler la sélection naturelle par la compétition.

| Propriété      | Détails                                                                             |
| :------------- | :---------------------------------------------------------------------------------- |
| **Dimensions** | Variable entre **200px** et **400px** (côté).                                       |
| **Mobilité**   | Déplacement aléatoire toutes les **70 à 250 frames**.                               |
| **Rôle**       | Augmente la **densité** de nourriture d'une zone afin de favoriser les Minos mobile |
