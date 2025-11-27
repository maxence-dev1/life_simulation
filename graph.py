import matplotlib.pyplot as plt





def graph(data):
    x = data[0]
    colors = plt.cm.tab10  # Palette de 10 couleurs différentes

    for idx, y in enumerate(data[1]):
        plt.plot(
            x,
            y,
            linewidth=1,         # ligne plus fine
            alpha=0.8,           # transparence légère
            color=colors(idx % 10),  # couleur différente
            label=f"mino {idx+1}"
        )

    plt.title("Exemple de graphique")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()

    # Afficher
    plt.show()
