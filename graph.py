import matplotlib.pyplot as plt
import matplotlib.cm as cm

fig, ax = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Répartition des attributs", fontsize=16)
def histogramme(i, j, data, titre="Histogramme sans titre"):
    ax[i,j].hist(data, bins="auto", alpha=0.7, edgecolor="black")
    ax[i,j].set_title(titre)
    ax[i,j].set_xlabel("Valeurs")
    ax[i,j].set_ylabel("Fréquence")

def graph(data):
    x = data[0]          # Les frames
    y_values = data[1]   # Liste des valeurs pour chaque mino
    
    colors = cm.tab10    # Palette de couleurs

    for idx, y in enumerate(y_values):
        ax[0,1].plot(
            x, y, 
            linewidth=1,
            alpha=0.8,
            color=colors(idx % 10),
            label=f"Mino {idx+1}"
        )

    ax[0,1].set_title("Évolution de la jauge faim")
    ax[0,1].set_xlabel("Frame")
    ax[0,1].set_ylabel("Jauge faim")
    ax[0,1].legend()

# 👉 Toujours à faire une seule fois à la fin
def print_graph_stat_repartition(resistance, vitesse, satiete, vision):
    histogramme(0,0,resistance, "resistance")
    histogramme(0,1,vitesse, "vitesse")
    histogramme(1,0,satiete, "satiete")
    histogramme(1,1,vision, "vision")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
