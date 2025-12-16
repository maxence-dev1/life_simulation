import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Button, RadioButtons
import numpy as np


class GraphStatistics:
    def __init__(self, df, food_data):
        self.setup_theme()
        self.graph_ax = None
        self.fig = None
        self.radio_ref = None
        self.btn_refs = []

        self.global_resistance = df["resistance"]
        self.global_vitesse = df["vitesse"]
        self.global_satiete = df["satiete"]
        self.global_vision = df["vision"]
        self.global_food_data = food_data
        self.global_time_lived = df["time_lived"]
        self.global_resistance_norme = None
        self.global_vitesse_norme = None
        self.global_satiete_norme = None
        self.global_vision_norme = None
        self.global_best = df.loc[df["time_lived"].idxmax()]
        self.global_worst = df.loc[df["time_lived"].idxmin()]

    @staticmethod
    def setup_theme():
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

    @staticmethod
    def normaliser(x,minimum,maximum):
     return (x-minimum)/(maximum - minimum)
    
    def get_norme_data(self):
        a = min(self.global_resistance)
        b = max(self.global_resistance)
        self.global_resistance_norme = self.global_resistance.apply(lambda x: self.normaliser(x, a, b))
        a = min(self.global_vitesse)
        b = max(self.global_vitesse)
        self.global_vitesse_norme = self.global_vitesse.apply(lambda x: self.normaliser(x, a, b))
        a = min(self.global_satiete)
        b = max(self.global_satiete)
        self.global_satiete_norme = self.global_satiete.apply(lambda x: self.normaliser(x, a, b))
        a = min(self.global_vision)
        b = max(self.global_vision)
        self.global_vision_norme = self.global_vision.apply(lambda x: self.normaliser(x, a, b))



    def clean_axes(self, ax):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, zorder=0)

    def histogramme(self, data, titre="Histogramme", color=None):
        if color is None:
            color = self.COLORS['res']
        self.graph_ax.cla()
        self.graph_ax.hist(data, bins="auto", alpha=0.8, color=color, edgecolor='#1e1e1e', linewidth=1.2, zorder=3)
        self.graph_ax.set_title(titre, fontsize=14, fontweight='bold', pad=15)
        self.graph_ax.set_xlabel("Valeurs", fontsize=11)
        self.graph_ax.set_ylabel("Fréquence", fontsize=11)
        self.clean_axes(self.graph_ax)
        plt.draw()

    def histogramme_best_worst(self, data, titre="Stats"):
        cat_colors = [self.COLORS['res'], self.COLORS['vit'], self.COLORS['sat'], self.COLORS['vis']]
        labels = ["Résistance", "Vitesse", "Satiété", "Vision"]
        x = range(len(data))

        self.graph_ax.cla()
        bars = self.graph_ax.bar(x, data, color=cat_colors, alpha=0.9, width=0.6, zorder=3)

        for bar in bars:
            height = bar.get_height()
            self.graph_ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                          f'{height:.2f}', ha='center', va='bottom', color='white', fontsize=10)

        self.graph_ax.set_xticks(x)
        self.graph_ax.set_xticklabels(labels, fontsize=11)
        self.graph_ax.set_title(titre, fontsize=16, fontweight='bold', pad=20)
        self.graph_ax.set_ylim(0, 1.1)
        self.graph_ax.get_yaxis().set_visible(False)

        for spine in self.graph_ax.spines.values():
            spine.set_visible(False)

        plt.draw()

    def graph(self, data, titre="Evolution"):
        self.graph_ax.cla()
        d = np.array(data)
        self.graph_ax.plot(d.T, color=self.COLORS['sat'], alpha=0.15, linewidth=1)
        mean_data = np.mean(d, axis=0)
        self.graph_ax.plot(mean_data, color='white', alpha=1, linewidth=2, linestyle='--', label="Moyenne")
        self.graph_ax.set_title(titre, fontsize=14, pad=15)
        self.graph_ax.set_xlabel("Frames (Temps)", fontsize=11)
        self.graph_ax.set_ylabel("nourriture", fontsize=11)
        self.graph_ax.legend(frameon=False)
        self.clean_axes(self.graph_ax)
        plt.draw()

    def active_survie_interactive(self, event):
        self.graph_ax.cla()
        self.clean_axes(self.graph_ax)

        ax_radio = plt.axes([0.78, 0.60, 0.12, 0.20], facecolor='#2b2b2b')
        labels = ['Résistance', 'Vitesse', 'Satiété', 'Vision']
        self.radio_ref = RadioButtons(ax_radio, labels, active=0, activecolor=self.COLORS['res'])

        if ax_radio.collections:
            circles = ax_radio.collections[0]
            circles.set_edgecolor(self.COLORS['txt_btn'])
            circles.set_sizes([100] * len(labels))

        for text in ax_radio.texts:
            text.set_color(self.COLORS['txt_btn'])
            text.set_fontsize(9)

        def update_graph(label):
            self.graph_ax.cla()
            idx = labels.index(label)
            
            mapping = {
                'Résistance': (self.global_resistance_norme, self.COLORS['res']),
                'Vitesse': (self.global_vitesse_norme, self.COLORS['vit']),
                'Satiété': (self.global_satiete_norme, self.COLORS['sat']),
                'Vision': (self.global_vision_norme, self.COLORS['vis'])
            }
            data, col = mapping[label]
            print("len(data) : ",len(data),"len(col) : ", len(col))

            if ax_radio.collections:
                new_colors = [self.COLORS['bg_btn']] * len(labels)
                new_colors[idx] = col
                ax_radio.collections[0].set_facecolors(new_colors)

            self.graph_ax.scatter(self.global_time_lived, data, color=col, alpha=0.6, s=30, edgecolors='none')

            if len(self.global_time_lived) > 1:
                try:
                    z = np.polyfit(self.global_time_lived, data, 1)
                    p = np.poly1d(z)
                    self.graph_ax.plot(self.global_time_lived, p(self.global_time_lived), "w--", alpha=0.5, linewidth=1, label="Tendance")
                except:
                    pass

            self.graph_ax.set_title(f"Corrélation : Survie vs {label}", fontsize=14, fontweight='bold', pad=15)
            self.graph_ax.set_xlabel("Temps vécu (Frames)", fontsize=11)
            self.graph_ax.set_ylabel(f"Valeur : {label}", fontsize=11)
            self.graph_ax.legend(loc='lower right', frameon=False)
            self.clean_axes(self.graph_ax)
            plt.draw()

        self.radio_ref.on_clicked(update_graph)
        update_graph('Résistance')

    def show_resistance(self, event):
        self.histogramme(self.global_resistance, "Distribution : Résistance", self.COLORS['res'])

    def show_vitesse(self, event):
        self.histogramme(self.global_vitesse, "Distribution : Vitesse", self.COLORS['vit'])

    def show_satiete(self, event):
        self.histogramme(self.global_satiete, "Distribution : Satiété", self.COLORS['sat'])

    def show_vision(self, event):
        self.histogramme(self.global_vision, "Distribution : Vision", self.COLORS['vis'])

    def show_faim(self, event):
        self.graph(self.global_food_data, "Dynamique de la faim (Population)")

    def show_best(self, event):
        self.histogramme_best_worst([
            self.normaliser(self.global_best["resistance"],min(self.global_resistance), max(self.global_resistance)),
            self.normaliser(self.global_best["vitesse"],min(self.global_vitesse), max(self.global_vitesse)),
            self.normaliser(self.global_best["satiete"],min(self.global_satiete), max(self.global_satiete)),
            self.normaliser(self.global_best["vision"],min(self.global_vision), max(self.global_vision))

        ], "Profil du CHAMPION")

    def show_worst(self, event):
        self.histogramme_best_worst([
            self.normaliser(self.global_worst["resistance"],min(self.global_resistance), max(self.global_resistance)),
            self.normaliser(self.global_worst["vitesse"],min(self.global_vitesse), max(self.global_vitesse)),
            self.normaliser(self.global_worst["satiete"],min(self.global_satiete), max(self.global_satiete)),
            self.normaliser(self.global_worst["vision"],min(self.global_vision), max(self.global_vision))
        ], "Profil du PIRE")

    def menu_statistique(self,):
        self.get_norme_data()
        self.fig, self.graph_ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.25, top=0.90, left=0.1, right=0.90)

        self.graph_ax.text(0.5, 0.5, "Sélectionnez une métrique ci-dessous",
                      ha='center', va='center', fontsize=16, color='#666666')
        self.graph_ax.set_axis_off()

        btn_height, btn_width = 0.06, 0.15
        y_row1, y_row2 = 0.12, 0.04
        spacing = 0.05
        start_x = (1 - (4 * btn_width + 3 * spacing)) / 2

        buttons_config = [
            {'label': 'Résistance', 'pos': [start_x, y_row1], 'color': self.COLORS['bg_btn'], 'func': self.show_resistance},
            {'label': 'Vitesse', 'pos': [start_x + btn_width + spacing, y_row1], 'color': self.COLORS['bg_btn'], 'func': self.show_vitesse},
            {'label': 'Satiété', 'pos': [start_x + 2*(btn_width + spacing), y_row1], 'color': self.COLORS['bg_btn'], 'func': self.show_satiete},
            {'label': 'Vision', 'pos': [start_x + 3*(btn_width + spacing), y_row1], 'color': self.COLORS['bg_btn'], 'func': self.show_vision},
            {'label': 'Temps Vécu', 'pos': [start_x, y_row2], 'color': '#444444', 'func': self.active_survie_interactive},
            {'label': 'Graph Faim', 'pos': [start_x + btn_width + spacing, y_row2], 'color': '#444444', 'func': self.show_faim},
            {'label': 'CHAMPION', 'pos': [start_x + 2*(btn_width + spacing), y_row2], 'color': '#2e7d32', 'func': self.show_best},
            {'label': 'PIRE', 'pos': [start_x + 3*(btn_width + spacing), y_row2], 'color': '#c62828', 'func': self.show_worst},
        ]

        for cfg in buttons_config:
            ax_btn = plt.axes([cfg['pos'][0], cfg['pos'][1], btn_width, btn_height])
            b = Button(ax_btn, cfg['label'], color=cfg['color'], hovercolor=self.COLORS['hover'])
            b.label.set_color(self.COLORS['txt_btn'])
            b.label.set_fontsize(9)
            b.on_clicked(cfg['func'])

            for spine in ax_btn.spines.values():
                spine.set_visible(False)

            self.btn_refs.append(b)

        plt.show()