import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Button, RadioButtons
import numpy as np



plt.rcParams.update({
    'figure.facecolor': '#1e1e1e',       
    'axes.facecolor': '#1e1e1e',         
    'axes.edgecolor': '#444444',         
    'axes.labelcolor': '#dddddd',        
    'text.color': '#dddddd',             
    'xtick.color': '#cccccc',            
    'ytick.color': '#cccccc',            
    'grid.color': '#444444',             
    'grid.linestyle': '--',              
    'grid.alpha': 0.5,                   
    'font.family': 'sans-serif',         
    'font.size': 10
})

COLORS = {
    'res': '#4fc3f7',   
    'vit': '#f06292',   
    'sat': '#aed581',   
    'vis': '#b39ddb',   
    'bg_btn': '#333333', 
    'txt_btn': 'white',  
    'hover': '#555555'   
}


graph_ax = None
fig = None
radio_ref = None 


def clean_axes(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, zorder=0)



def histogramme(data, titre="Histogramme", color=COLORS['res']):
    graph_ax.cla()
    graph_ax.hist(data, bins="auto", alpha=0.8, color=color, edgecolor='#1e1e1e', linewidth=1.2, zorder=3)
    graph_ax.set_title(titre, fontsize=14, fontweight='bold', pad=15)
    graph_ax.set_xlabel("Valeurs", fontsize=11)
    graph_ax.set_ylabel("Fréquence", fontsize=11)
    clean_axes(graph_ax)
    plt.draw()

def histogramme_best_worst(data, titre="Stats"):
    cat_colors = [COLORS['res'], COLORS['vit'], COLORS['sat'], COLORS['vis']]
    labels = ["Résistance", "Vitesse", "Satiété", "Vision"]
    x = range(len(data))
    
    graph_ax.cla()
    bars = graph_ax.bar(x, data, color=cat_colors, alpha=0.9, width=0.6, zorder=3)
    
    for bar in bars:
        height = bar.get_height()
        graph_ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                      f'{height:.2f}', ha='center', va='bottom', color='white', fontsize=10)

    graph_ax.set_xticks(x)
    graph_ax.set_xticklabels(labels, fontsize=11)
    graph_ax.set_title(titre, fontsize=16, fontweight='bold', pad=20)
    graph_ax.set_ylim(0, 1.1)
    graph_ax.get_yaxis().set_visible(False)
    
    for spine in graph_ax.spines.values():
        spine.set_visible(False)
        
    plt.draw()

def graph(data, titre="Evolution"):
    graph_ax.cla()
    d = np.array(data)
    graph_ax.plot(d.T, color=COLORS['sat'], alpha=0.15, linewidth=1)
    mean_data = np.mean(d, axis=0)
    graph_ax.plot(mean_data, color='white', alpha=1, linewidth=2, linestyle='--', label="Moyenne")
    graph_ax.set_title(titre, fontsize=14, pad=15)
    graph_ax.set_xlabel("Frames (Temps)", fontsize=11)
    graph_ax.set_ylabel("nourriture", fontsize=11)
    graph_ax.legend(frameon=False)
    clean_axes(graph_ax)
    plt.draw()

def active_survie_interactive(event):
    """Initialise la vue interactive pour le temps de survie"""
    global radio_ref, graph_ax
    
    graph_ax.cla()
    clean_axes(graph_ax)
    
    ax_radio = plt.axes([0.78, 0.60, 0.12, 0.20], facecolor='#2b2b2b') 
    
    labels = ['Résistance', 'Vitesse', 'Satiété', 'Vision']
    radio_ref = RadioButtons(ax_radio, labels, active=0, activecolor=COLORS['res'])
    
    if ax_radio.collections:
        circles = ax_radio.collections[0]
        circles.set_edgecolor(COLORS['txt_btn']) 
        circles.set_sizes([100] * len(labels)) 
        
    for text in ax_radio.texts:
        text.set_color(COLORS['txt_btn'])
        text.set_fontsize(9)

    def update_graph(label):
        graph_ax.cla()
        
        idx = labels.index(label)
        if label == 'Résistance':
            data, col = global_resistance_norme, COLORS['res']
        elif label == 'Vitesse':
            data, col = global_vitesse_norme, COLORS['vit']
        elif label == 'Satiété':
            data, col = global_satiete_norme, COLORS['sat']
        else: 
            data, col = global_vision_norme, COLORS['vis']
            

        if ax_radio.collections:
            new_colors = [COLORS['bg_btn']] * len(labels)
            new_colors[idx] = col
            ax_radio.collections[0].set_facecolors(new_colors)

        graph_ax.scatter(global_time_lived, data, color=col, alpha=0.6, s=30, edgecolors='none')
        
        if len(global_time_lived) > 1:
            try:
                z = np.polyfit(global_time_lived, data, 1)
                p = np.poly1d(z)
                graph_ax.plot(global_time_lived, p(global_time_lived), "w--", alpha=0.5, linewidth=1, label="Tendance")
            except:
                pass

        graph_ax.set_title(f"Corrélation : Survie vs {label}", fontsize=14, fontweight='bold', pad=15)
        graph_ax.set_xlabel("Temps vécu (Frames)", fontsize=11)
        graph_ax.set_ylabel(f"Valeur : {label}", fontsize=11)
        graph_ax.legend(loc='lower right', frameon=False)
        clean_axes(graph_ax)
        plt.draw()


    radio_ref.on_clicked(update_graph)
    update_graph('Résistance')


def show_resistance(event): histogramme(global_resistance, "Distribution : Résistance", COLORS['res'])
def show_vitesse(event):    histogramme(global_vitesse, "Distribution : Vitesse", COLORS['vit'])
def show_satiete(event):    histogramme(global_satiete, "Distribution : Satiété", COLORS['sat'])
def show_vision(event):     histogramme(global_vision, "Distribution : Vision", COLORS['vis'])
def show_faim(event):       graph(global_food_data, "Dynamique de la faim (Population)")

def show_best(event):
    histogramme_best_worst([global_best["resistance_normee"], global_best["vitesse_normee"], global_best["satiete_normee"], global_best["vision_normee"]], "Profil du CHAMPION")

def show_worst(event):
    histogramme_best_worst([global_worst["resistance_normee"], global_worst["vitesse_normee"], global_worst["satiete_normee"], global_worst["vision_normee"]], "Profil du PIRE")


def menu_statistique(df, food_data):

    global global_resistance, global_vitesse, global_satiete, global_vision, global_food_data, graph_ax, global_time_lived, global_resistance_norme, global_vitesse_norme, global_satiete_norme, global_vision_norme, global_best, global_worst, fig, btn_refs
    
    global_resistance = df["resistance"]
    global_vitesse = df["vitesse"]
    global_satiete = df["satiete"]
    global_vision = df["vision"]
    global_food_data = food_data
    global_time_lived = df["temps vécu"]
    global_resistance_norme = df["resistance_normee"]
    global_vitesse_norme = df["vitesse_normee"]
    global_satiete_norme = df["satiete_normee"]
    global_vision_norme = df["vision_normee"]
    global_best = df.loc[df["temps vécu"].idxmax()]
    global_worst = df.loc[df["temps vécu"].idxmin()]
    
    fig, graph_ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(bottom=0.25, top=0.90, left=0.1, right=0.90) 

    graph_ax.text(0.5, 0.5, "Sélectionnez une métrique ci-dessous", 
                  ha='center', va='center', fontsize=16, color='#666666')
    graph_ax.set_axis_off()

    btn_height, btn_width = 0.06, 0.15
    y_row1, y_row2 = 0.12, 0.04
    spacing = 0.05
    start_x = (1 - (4 * btn_width + 3 * spacing)) / 2 

    buttons_config = [
        {'label': 'Résistance', 'pos': [start_x, y_row1], 'color': COLORS['bg_btn'], 'func': show_resistance},
        {'label': 'Vitesse',    'pos': [start_x + btn_width + spacing, y_row1], 'color': COLORS['bg_btn'], 'func': show_vitesse},
        {'label': 'Satiété',    'pos': [start_x + 2*(btn_width + spacing), y_row1], 'color': COLORS['bg_btn'], 'func': show_satiete},
        {'label': 'Vision',     'pos': [start_x + 3*(btn_width + spacing), y_row1], 'color': COLORS['bg_btn'], 'func': show_vision},
        
        {'label': 'Temps Vécu', 'pos': [start_x, y_row2], 'color': '#444444', 'func': active_survie_interactive},
        {'label': 'Graph Faim', 'pos': [start_x + btn_width + spacing, y_row2], 'color': '#444444', 'func': show_faim},
        {'label': 'CHAMPION',   'pos': [start_x + 2*(btn_width + spacing), y_row2], 'color': '#2e7d32', 'func': show_best},
        {'label': 'PIRE',       'pos': [start_x + 3*(btn_width + spacing), y_row2], 'color': '#c62828', 'func': show_worst},
    ]
    
    btn_refs = [] 

    for cfg in buttons_config:
        ax_btn = plt.axes([cfg['pos'][0], cfg['pos'][1], btn_width, btn_height])
        b = Button(ax_btn, cfg['label'], color=cfg['color'], hovercolor=COLORS['hover'])
        b.label.set_color(COLORS['txt_btn'])
        b.label.set_fontsize(9)
        b.on_clicked(cfg['func'])
        
        for spine in ax_btn.spines.values(): spine.set_visible(False)
        
        btn_refs.append(b)

    plt.show()