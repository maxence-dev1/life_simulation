import matplotlib.pyplot as plt

# Exemple de données
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Créer le graphique
plt.plot(x, y, marker='o', linestyle='-', color='blue', label="y = f(x)")

# Ajouter titre et labels
plt.title("Exemple de graphique")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

# Afficher
plt.show()
