import pygame, sys, draw, minos, time, random, food, pygame_menu, graph, pygame_gui, numpy, simulationconfig, simulationengine
import pandas as pd
#5000 minos avec 0 food avant opti : afficher->1.13 sans afficher -> 9 sec
#1000 minos avec 500 food avant opti : afficher->4.07 sans afficher -> 2.46 min (variable car la simulation n'a jamais 0 food dépend donc des attributs des minos)

#5000 minos avec 0 food apres opti : afficher->1.28 sans afficher -> 25 sec
#1000 minos avec 500 food apres opti : afficher->1.32 sans afficher -> 37 sec


def main(nb_minos = None, ratio_food = None, width = 2000, height = 1000):
    pygame.init()
    if nb_minos is None:

        WIDTH = 1200
        HEIGHT = 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        manager = pygame_gui.UIManager((WIDTH,HEIGHT), theme_path='theme.json')
        clock = pygame.time.Clock()


        pygame.display.set_caption("life simulation")
        pygame.event.pump()

        state_menu = [True] #Ici j'ai mis des listes afin de pouvoir modifier directement la variable à l'adresse depuis d'autres fonctions
        running = [False]

        config = simulationconfig.SimulationConfig(screen, state_menu, running)


        frame_fps = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 210, 60), 
            manager=manager,
        )

        button_less_fps = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(5, 15, 35, 30),
            text="-",
            manager=manager,
            container=frame_fps
        )


        label_fps = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 15, 90, 30),
            text=f"FPS : {clock.get_fps():.1f}/{config.fps}", 
            manager=manager,
            container=frame_fps
        )

        button_more_fps = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(160, 15, 35, 30),
            text="+",
            manager=manager,
            container=frame_fps
        )



        config.init_all()



        while state_menu[0]:
            screen.fill((0,0,0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    state_menu[0] = False
            config.menu_update(events)
            
            


        if config.full_screen: 
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            WIDTH = pygame.display.Info().current_w
            HEIGHT = pygame.display.Info().current_h


        d = draw.Draw(screen, WIDTH, HEIGHT)
        engine = simulationengine.Engine(WIDTH, HEIGHT, config.ratio_food, running, d)
        engine.init_grid()
        engine.init_food_list()
        engine.init_gui(f"FPS : 0/{config.fps}")
        engine.init_minos(config.nb_minos, config.size_minos,config.resistance_mu, config.resistance_sigma, config.vitesse_mu, config.vitesse_sigma, config.satiete_mu, config.satiete_sigma, config.vision_mu, config.vision_sigma, config.print_vision)




        text_pas_affichage = pygame.font.Font(None, 36).render("Simulation en cours, veuillez patienter", True, "white")
        one = True



        while running:
            time_delta = clock.tick(config.fps)/1000
            
            engine.update_food()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                manager.process_events(event)
                if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == button_more_fps):
                    config.more_fps()
                elif (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == button_less_fps):
                        config.less_fps()

                
            engine.update_all_minos(config.afficher_jeu)
            # if engine.nb_frame%60 == 0:
            #     print("minos morts : ", engine.minos_dead,"/", config.nb_minos-1)
            if engine.minos_dead == config.nb_minos-1:
                running = False
            
            if config.afficher_jeu:
                engine.print_grid(config.print_grille)
                d.draw_all_mino(engine.minos_list)
                d.draw_all_food(engine.food_list)
                manager.update(time_delta)
                manager.draw_ui(screen)
                label_fps.set_text(f"FPS : {clock.get_fps():.1f}/{config.fps}")
                d.refresh()
            
                
            else : 
                d.fill_screen((0,0,0))
                screen.blit(text_pas_affichage, (100,200))
                
                if one: 
                    pygame.display.flip()
                    one = False






        df_minos = pd.DataFrame(engine.minos_list_id, columns=["id", "resistance", "vitesse", "satiete", "vision", "time_lived"])
        g = graph.GraphStatistics(df_minos, engine.food_data)


        g.menu_statistique()


        pygame.quit()
        sys.exit()

    else:
        clock = pygame.time.Clock()


        pygame.display.set_caption("life simulation")
        pygame.event.pump()

        state_menu = [True] #Ici j'ai mis des listes afin de pouvoir modifier directement la variable à l'adresse depuis d'autres fonctions
        running = [False]

        config = simulationconfig.SimulationConfig(None, state_menu, running)
        config.fps = -1




        config.init_all(False)
        config.nb_minos = nb_minos

        engine = simulationengine.Engine(width, height, config.ratio_food, running, None)
        engine.init_grid()
        engine.init_food_list()
        engine.init_minos(config.nb_minos, config.size_minos,config.resistance_mu, config.resistance_sigma, config.vitesse_mu, config.vitesse_sigma, config.satiete_mu, config.satiete_sigma, config.vision_mu, config.vision_sigma, config.print_vision)
        engine.ratio_food = ratio_food




        while running:
            time_delta = clock.tick(config.fps)/1000
            engine.update_food()
            engine.update_all_minos(False)
            if engine.minos_dead == config.nb_minos-1:
                running = False

        df_minos = pd.DataFrame(engine.minos_list_id, columns=["id", "resistance", "vitesse", "satiete", "vision", "time_lived"])
        return (df_minos, engine.food_data)

