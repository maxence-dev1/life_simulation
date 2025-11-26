import matplotlib.pyplot as plt





def graph(data):
    x = data[0]
    y = data[1]

    # Créer le graphique
    plt.plot(x, y, marker='o', linestyle='-', color='blue', label="y = f(x)")

    # Ajouter titre et labels
    plt.title("Exemple de graphique")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()

    # Afficher
    plt.show()
