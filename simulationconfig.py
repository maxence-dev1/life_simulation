import pygame, pygame_gui, pygame_menu

class SimulationConfig:
    def __init__(self, screen, state_mene, running):
        self.full_screen = False
        self.print_vision = True
        self.afficher_jeu = True
        self.nb_minos = 20
        self.size_minos = 30
        self.nb_food = 5
        self.resistance_mu = 2
        self.resistance_sigma = 0.5
        self.vitesse_mu = 5
        self.vitesse_sigma = 1.5
        self.satiete_mu = 1
        self.satiete_sigma = 0.75
        self.vision_mu = 150
        self.vision_sigma = 120
        self.print_grille = False
        self.fps = 50
        self.screen = screen
        self.state_menu = state_mene
        self.running = running
        self.menu = pygame_menu.Menu(
            width=1200,
            height=800,
            title="Menu Principal",
            theme=pygame_menu.themes.THEME_DARK
        )


    def start(self):
        self.state_menu[0] = False
        self.running[0] = 1 


    
    def more_fps(self):
        self.fps += 1

    def less_fps(self):
        self.fps -= 1

    def init_all(self):

        self.menu.add.button("Jouer", self.start)
        self.menu.add.button("Quitter", pygame_menu.events.EXIT)

        self.menu.add.toggle_switch(
            title="Plein écran : ",
            default=False,
            # Correct : n'attend qu'un seul argument (value)
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
            "size minos : ",
            default=str(self.size_minos),
            input_type=pygame_menu.locals.INPUT_INT,
            onchange=lambda value: setattr(self, "size_minos", int(value))
        )

        self.menu.add.text_input(
            "nombre food : ",
            default=str(self.nb_food),
            input_type=pygame_menu.locals.INPUT_INT,
            onchange=lambda value: setattr(self, "nb_food", int(value))
        )


        self.menu.add.toggle_switch(
            title="Afficher vision :",
            default=self.print_vision,
            # Correct : n'attend qu'un seul argument (value)
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

    def menu_update(self, events):
        self.menu.update(events)
        self.menu.draw(self.screen)
        pygame.display.flip()