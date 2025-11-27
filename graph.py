import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Button

# Création de la figure
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.22)  # espace pour les boutons

# Axe pour le graphe
graph_ax = None

def histogramme(data, titre="Histogramme sans titre", color = "blue"):
    graph_ax.clear()
    graph_ax.hist(data, bins="auto", alpha=0.7, edgecolor="black", color = color)
    graph_ax.set_title(titre)
    graph_ax.set_xlabel("Valeurs")
    graph_ax.set_ylabel("Fréquence")
    plt.draw()

def graph(data, titre = "graphique sans titre"):
    graph_ax.clear()
    for d in data:
        graph_ax.plot( range(len(data[0])), d)
    graph_ax.set_title(titre)
    graph_ax.set_xlabel("Frames")
    graph_ax.set_ylabel("Jauge nourriture")

    
    plt.draw()
    




import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.cm as cm

plt.close("all")


# --- GRAPHIQUES STATIQUES ---

def show_resistance(event):
    histogramme(global_resistance, "Résistance", "blue")

def show_vitesse(event):
    histogramme(global_vitesse, "Vitesse", "red")

def show_satiete(event):
    histogramme(global_satiete, "Satiété", "orange")

def show_vision(event):
    histogramme(global_vision, "Vision", "purple")

def show_faim(event):
    graph(global_food_data, "Évolution de la faim")



# --- INTERFACE DE CHOIX ---

def menu_statistique(resistance, vitesse, satiete, vision, food_data):

    global global_resistance, global_vitesse, global_satiete, global_vision, global_food_data
    global_resistance = resistance
    global_vitesse = vitesse
    global_satiete = satiete
    global_vision = vision
    global_food_data = food_data

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.35)

    global graph_ax
    graph_ax = fig.add_subplot(111)  # crée un axe propre

    graph_ax.set_title("Choisissez un graphique ci-dessous")


    # Placement des boutons
    ax_res = plt.axes([0.05, 0.15, 0.18, 0.1])
    ax_vit = plt.axes([0.27, 0.15, 0.18, 0.1])
    ax_sat = plt.axes([0.49, 0.15, 0.18, 0.10])
    ax_vis = plt.axes([0.71, 0.15, 0.18, 0.10])
    
    ax_food = plt.axes([0.3, 0.02, 0.4, 0.1])


    # Création des boutons
    btn_res = Button(ax_res, "Résistance")
    btn_vit = Button(ax_vit, "Vitesse")
    btn_sat = Button(ax_sat, "Satiété")
    btn_vis = Button(ax_vis, "Vision")
    btn_food = Button(ax_food, "Graph Faim")

    # Bind événements
    btn_res.on_clicked(show_resistance)
    btn_vit.on_clicked(show_vitesse)
    btn_sat.on_clicked(show_satiete)
    btn_vis.on_clicked(show_vision)
    btn_food.on_clicked(show_faim)

    plt.show()

