import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Button

# Création de la figure
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.22)  # espace pour les boutons

# Axe pour le graphe
graph_ax = plt.gca()

def histogramme(data, titre="Histogramme sans titre", color = "blue"):
    graph_ax.clear()
    graph_ax.hist(data, bins="auto", alpha=0.7, edgecolor="black", color = color)
    graph_ax.set_title(titre)
    graph_ax.set_xlabel("Valeurs")
    graph_ax.set_ylabel("Fréquence")
    plt.draw()




# 👉 Toujours à faire une seule fois à la fin
def print_graph_stat_repartition(resistance, vitesse, satiete, vision):
    
    # Création des boutons
    ax_res = plt.axes([0.1, 0.05, 0.15, 0.075])  # [left, bottom, width, height]
    ax_vit = plt.axes([0.3, 0.05, 0.15, 0.075])
    ax_sat = plt.axes([0.5, 0.05, 0.15, 0.075])
    ax_vis = plt.axes([0.7, 0.05, 0.15, 0.075])

    btn_res = Button(ax_res, "Résistance")
    btn_vit = Button(ax_vit, "Vitesse")
    btn_sat = Button(ax_sat, "Satiété")
    btn_vis = Button(ax_vis, "Vision")

    histogramme(resistance, "resistance", "blue")

    btn_res.on_clicked(lambda event: histogramme(resistance, "resistance", "blue"))
    btn_vit.on_clicked(lambda event: histogramme(vitesse, "Vitesse", "red"))
    btn_sat.on_clicked(lambda event: histogramme(satiete, "Satiete", "yellow"))
    btn_vis.on_clicked(lambda event: histogramme(vision, "vition", "grey"))

    plt.show()

