import pygame, pygame_gui, pygame_menu

class SimulationConfig:
    def __init__(self,width, height, screen = None, state_mene =None, running = None):
        self.full_screen = False
        self.print_vision = False
        self.afficher_jeu = True
        self.nb_minos = 100
        self.ratio_food = 0.3
        self.resistance_mu = 2
        self.resistance_sigma = 1
        self.vitesse_mu = 6
        self.vitesse_sigma = 3
        self.satiete_mu = 1.2
        self.satiete_sigma = 0.4
        self.vision_mu = 200
        self.vision_sigma = 100
        self.print_grille = False
        self.fps = 20
        self.abundance_zone = False
        self.screen = screen
        self.state_menu = state_mene
        self.running = running
        self.width = width
        self.height = height
        
        
        self.my_theme = pygame_menu.themes.THEME_DARK.copy()
        self.my_theme.background_color = (25, 27, 30)       
        self.my_theme.title_background_color = (35, 38, 42) 
        self.my_theme.title_font_color = (220, 220, 220)    
        self.my_theme.widget_font_color = (180, 180, 180)   
        self.my_theme.selection_color = (70, 130, 180)      

        self.my_theme.title_font = pygame_menu.font.FONT_BEBAS  
        self.my_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
        self.my_theme.widget_font_size = 22
        self.my_theme.title_font_size = 35
        self.my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE


        self.my_theme.widget_cursor = pygame_menu.locals.CURSOR_HAND 
        self.my_theme.widget_margin = (0, 15)      

        self.menu = pygame_menu.Menu(
            width=width,
            height=height,
            title="Menu Principal",
            theme=self.my_theme)


    def start(self):
        if not self.afficher_jeu:
            self.fps = -1
        self.state_menu[0] = False
        if self.running is not None:
            self.running[0] = True 


    
    def more_fps(self):
        self.fps += 1

    def less_fps(self):
        self.fps -= 1



    def init_all(self, interface = True):
        if not interface:
            self.running[0] = True
            return
        self.menu.add.button("Jouer", self.start)
        self.menu.add.button("Quitter", pygame_menu.events.EXIT)

        self.menu.add.toggle_switch(
            title="Plein écran : ",
            default=False,
            onchange=lambda value: setattr(self, "full_screen", value),
            width=60
        )

        self.menu.add.text_input(
            "nombre minos : ",
            default=str(self.nb_minos),
            input_type=pygame_menu.locals.INPUT_INT,
            onchange=lambda value: setattr(self, "nb_minos", int(value))
        )
        self.menu.add.text_input(
            "ratio food (nombre de nourriture par mino) : ",
            default=str(self.ratio_food),
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda value: setattr(self, "ratio_food", float(value))
        )

        self.menu.add.toggle_switch(
            title="Abundance zone :",
            default=self.abundance_zone,
            onchange=lambda value: setattr(self, "abundance_zone", int(value)),
            width=60
        )


        self.menu.add.toggle_switch(
            title="Afficher vision :",
            default=self.print_vision,
            onchange=lambda value: setattr(self, "print_vision", int(value)),
            width=60
        )

        self.menu.add.toggle_switch(
            title="Afficher jeu (beaucoup moins de temps de simulation) :",
            default=self.afficher_jeu,
            # Correct : n'attend qu'un seul argument (value)
            onchange=lambda value: setattr(self, "afficher_jeu", int(value)),
            width=60
        )


        self.menu.add.text_input(
            "Resistance µ : ", 
            default=str(self.resistance_mu), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            # Si 'val' est vide, on utilise la valeur actuelle de resistance_mu[0]. Sinon, on convertit l'entrée en float.
            onchange=lambda val: setattr(self, "resistance_mu", float(val) if val else self.resistance_mu),
        )
        self.menu.add.text_input(
            "Resistance σ : ", 
            default=str(self.resistance_sigma), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda val: setattr(self, "resistance_sigma", float(val) if val else self.resistance_sigma),
        )
        self.menu.add.text_input(
            "Vitesse µ : ", 
            default=str(self.vitesse_mu), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda val: setattr(self, "vitesse_mu", float(val) if val else self.vitesse_mu),
        )
        self.menu.add.text_input(
            "Vitesse σ : ", 
            default=str(self.vitesse_sigma), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda val: setattr(self, "vitesse_sigma", float(val) if val else self.vitesse_sigma),
        )
        self.menu.add.text_input(
            "Satiété µ : ", 
            default=str(self.satiete_mu), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda val: setattr(self, "satiete_mu", float(val) if val else self.satiete_mu),
        )
        self.menu.add.text_input(
            "Satiété σ : ", 
            default=str(self.satiete_sigma), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda val: setattr(self, "satiete_sigma", float(val) if val else self.satiete_sigma),
        )
        self.menu.add.text_input(
            "Vision µ : ", 
            default=str(self.vision_mu), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda val: setattr(self, "vision_mu", float(val) if val else self.vision_mu),
        )
        self.menu.add.text_input(
            "Vision σ : ", 
            default=str(self.vision_sigma), 
            input_type=pygame_menu.locals.INPUT_FLOAT,
            onchange=lambda val: setattr(self, "vision_sigma", float(val) if val else self.vision_sigma),
        )
        
        self.menu.add.label("_____________________________________________________________", "Dev panel_l1")
        self.menu.add.label("DEV TOOLS", "DEV TOOLS")
        self.menu.add.label("_____________________________________________________________", "Dev panel_l2")

        self.menu.add.toggle_switch(
            title="Afficher grille :",
            default=self.print_grille,
            # Correct : n'attend qu'un seul argument (value)
            onchange=lambda val: setattr(self, "print_grille", val),
            width=60
        )

        self.menu.add.text_input(
            "FPS : ", 
            default=str(self.fps), 
            input_type=pygame_menu.locals.INPUT_INT,
            onchange=lambda val: setattr(self, "fps", int(val)),
        )

    def init_all_several_simulation(self, infos):
            self.menu.add.button("Jouer", self.start)
            self.menu.add.button("Quitter", pygame_menu.events.EXIT)
            self.menu.add.text_input(
                "nombre minos minimal: ",
                default=str(infos[0]),
                input_type=pygame_menu.locals.INPUT_INT,
                onchange=lambda value: infos.__setitem__(0, int(value) if value else 0)
            )
            self.menu.add.text_input(
                "nombre minos maximal: ",
                default=str(infos[1]),
                input_type=pygame_menu.locals.INPUT_INT,
                onchange=lambda value: infos.__setitem__(0, int(value) if value else 0)
            )
            self.menu.add.text_input(
                "pas nombre minos: ",
                default=str(infos[2]),
                input_type=pygame_menu.locals.INPUT_INT,
                onchange=lambda value: infos.__setitem__(0, int(value) if value else 0)
            )
            self.menu.add.text_input(
                "ratio food minimal: ",
                default=str(infos[3]),
                input_type=pygame_menu.locals.INPUT_INT,
                onchange=lambda value: infos.__setitem__(0, int(value) if value else 0)
            )
            self.menu.add.text_input(
                "ratio food maximal: ",
                default=str(infos[4]),
                input_type=pygame_menu.locals.INPUT_INT,
                onchange=lambda value: infos.__setitem__(0, int(value) if value else 0)
            )
            self.menu.add.text_input(
                "pas ratio food: ",
                default=str(infos[5]),
                input_type=pygame_menu.locals.INPUT_INT,
                onchange=lambda value: infos.__setitem__(0, int(value) if value else 0)
            )

            return

    def menu_update(self, events):
        self.menu.update(events)
        self.menu.draw(self.screen)
        pygame.display.flip()