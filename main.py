import pygame, sys, draw, minos, time, random, food, pygame_menu, graph, pygame_gui, numpy, simulationconfig, simulationengine
import pandas as pd
#5000 minos avec 0 food avant opti : afficher->1.13 sans afficher -> 9 sec
#1000 minos avec 500 food avant opti : afficher->4.07 sans afficher -> 2.46 min (variable car la simulation n'a jamais 0 food dépend donc des attributs des minos)

#5000 minos avec 0 food apres opti : afficher->1.28 sans afficher -> 25 sec
#1000 minos avec 500 food apres opti : afficher->1.32 sans afficher -> 37 sec
import ctypes
import os


try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()



def valider(running_mode_choice):
    running_mode_choice[0] = False

def toggle_one_simulation(one_simulation, switch_one, switch_several):
    one_simulation[0] = not one_simulation[0]
    switch_several.set_value(not one_simulation[0])
    switch_one.set_value(one_simulation[0])



my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.background_color = (25, 27, 30)       
my_theme.title_background_color = (35, 38, 42) 
my_theme.title_font_color = (220, 220, 220)    
my_theme.widget_font_color = (180, 180, 180)   
my_theme.selection_color = (70, 130, 180)      

my_theme.title_font = pygame_menu.font.FONT_BEBAS  
my_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
my_theme.widget_font_size = 22
my_theme.title_font_size = 35
my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE


my_theme.widget_cursor = pygame_menu.locals.CURSOR_HAND 
my_theme.widget_margin = (0, 15)                       

def main_mode_choice():
    pygame.init()
    one_simulation = [True]
    
    
    mode_choice_screen = pygame.display.set_mode((800, 600))
    mode_choice_menu = pygame_menu.Menu(
                width=800,
                height=600,
                title="Mode choice",
                theme=my_theme
            )
    
    
    
    mode_choice_menu.add.label("Veuillez choisir votre mode\n")
    mode_choice_menu.add.label("Simulation simple\n")
    switch_one = mode_choice_menu.add.toggle_switch(
            title="Faire une seule simulation ",
            default=one_simulation[0],
            onchange=lambda value: toggle_one_simulation(one_simulation, switch_one, switch_several),
            width=60
        )
    
    mode_choice_menu.add.label("several simulations ")
    switch_several =  mode_choice_menu.add.toggle_switch(
            title="Faire plusieurs simulations ",
            default= not one_simulation[0],
            onchange=lambda value: toggle_one_simulation(one_simulation, switch_one, switch_several),
            width=60
        )


    mode_choice_menu.add.button("Valider", lambda: valider(running_mode_choice))
    
    
    
    running_mode_choice = [True]
    while running_mode_choice[0]:
        mode_choice_screen.fill((0,0,0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running_mode_choice = False
        mode_choice_menu.update(events)
        mode_choice_menu.draw(mode_choice_screen)
        pygame.display.flip()
    
    if one_simulation[0]:
        print("main")
        main()
    else : 
        print("not main")
        several_simulations()


def several_simulations():
    state_menu = [True] 
    infos = [1,50,2,100,1,10] #mino min, minos max, minos pas, food min, food max, pas
    screen = pygame.display.set_mode((2000, 1000))
    config = simulationconfig.SimulationConfig(2000, 1000, screen, state_menu, None)
    config.init_all_several_simulation(infos)
    


    while state_menu[0]:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                state_menu[0] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    config.start()
            
        config.menu_update(events)
    
    big_data = []
    for nb_minos in range(infos[0],infos[1],infos[2]): 
        for ratio in range(infos[4],infos[3],infos[5]):
            res = main(nb_minos,1/ratio)
            df_sim = res[0]
            df_sim["nb_minos"] = nb_minos
            df_sim["ratio_food"] = 1/ratio
            big_data.append(df_sim)
            print(f"simulation avec {nb_minos} minos et 1/{ratio} ratio. time : {res[0]["time_lived"].max()}")


    final_big_df = pd.concat(big_data)
    final_big_df.to_csv("data.csv",header= True, index=False)



def main(nb_minos = None, ratio_food = None, width = 2000, height = 1000):
    pygame.init()
    if nb_minos is None:
        WIDTH = 1999
        HEIGHT = 1000
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        manager = pygame_gui.UIManager((WIDTH,HEIGHT), theme_path='theme.json')
        clock = pygame.time.Clock()


        pygame.display.set_caption("life simulation")
        pygame.event.pump()

        state_menu = [True] #Ici j'ai mis des listes afin de pouvoir modifier directement la variable à l'adresse depuis d'autres fonctions
        running = [False]

        config = simulationconfig.SimulationConfig(WIDTH, HEIGHT, screen, state_menu, running)

        config.init_all()
        


        while state_menu[0]:
            screen.fill((0,0,0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    state_menu[0] = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        config.start()
                
            config.menu_update(events)
            
            

        if config.full_screen and nb_minos == None : 
            WIDTH, HEIGHT = pygame.display.list_modes()[0]
            screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
            manager.set_window_resolution((WIDTH, HEIGHT)) 
        

        d = draw.Draw(screen, WIDTH, HEIGHT)
        
        engine = simulationengine.Engine(WIDTH, HEIGHT, config.ratio_food, running, d, False, screen, manager)
        
        engine.init_grid()
        engine.init_abundance_zone()
        
        engine.init_gui(f"FPS : 0/{config.fps}")
        engine.init_minos(config.nb_minos,config.resistance_mu, config.resistance_sigma, config.vitesse_mu, config.vitesse_sigma, config.satiete_mu, config.satiete_sigma, config.vision_mu, config.vision_sigma, config.print_vision)
        engine.init_food_list()
        


        text_pas_affichage = pygame.font.Font(None, 36).render("Simulation en cours, veuillez patienter", True, "white")
        one = True


        while running[0]:
            time_delta = clock.tick(config.fps)/1000
            
            engine.update_food()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running[0] = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running[0] = False
                manager.process_events(event)
                if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == engine.button_more_fps):
                    config.more_fps()
                elif (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == engine.button_less_fps):
                        config.less_fps()

                
            engine.update_all_minos(config.afficher_jeu)
            if config.abundance_zone:
                engine.update_abundance_zone()

            if engine.minos_dead == config.nb_minos:
                print("FINI")
                running[0] = False
            
            if config.afficher_jeu:
                engine.print_grid(config.print_grille)
                d.draw_all_mino(engine.minos_list)
                d.draw_all_food(engine.food_list)
                if config.abundance_zone:
                    engine.draw_abundance_zone()
                manager.update(time_delta)
                manager.draw_ui(screen)
                engine.label_fps.set_text(f"FPS : {clock.get_fps():.1f}/{config.fps}")
                d.refresh()
            
                
            else : 
                d.fill_screen((0,0,0))
                screen.blit(text_pas_affichage, (100,200))
                if engine.nb_frame%60 == 0:
                    print("minos morts : ", engine.minos_dead,"/", config.nb_minos-1)
                if one: 
                    pygame.display.flip()
                    one = False

        pd.set_option("display.max_rows", 100)
        df_minos = pd.DataFrame(engine.minos_list_id, columns=["id", "resistance", "vitesse", "satiete", "vision", "time_lived", "food_eaten", "distance_traveled"])
        df_minos["ratio_food"] = engine.ratio_food
        print(df_minos)
        id1 = df_minos["time_lived"].idxmax()
        print("best : ", engine.minos_list[id1].nb_time_in_abundance_zone)
        id2 = df_minos["time_lived"].idxmin()
        print("worst : ", engine.minos_list[id2].nb_time_in_abundance_zone)
        pd.set_option('display.max_rows', 100)
        g = graph.GraphStatistics(df_minos, engine.food_data)


        g.menu_statistique()


        pygame.quit()
        sys.exit()

    else:
        clock = pygame.time.Clock()

        
        running = [False]
        state_menu = [True] #Ici j'ai mis des listes afin de pouvoir modifier directement la variable à l'adresse depuis d'autres fonctions
        config = simulationconfig.SimulationConfig(width, height, None, state_menu, running)
        config.fps = -1
        config.nb_minos = nb_minos
        config.init_all(False)
        
        
        
        
        

        engine = simulationengine.Engine(width, height, config.ratio_food, running, None, True)
        engine.init_grid()
        
        engine.init_minos(config.nb_minos,config.resistance_mu, config.resistance_sigma, config.vitesse_mu, config.vitesse_sigma, config.satiete_mu, config.satiete_sigma, config.vision_mu, config.vision_sigma, config.print_vision)
        engine.init_food_list()
        engine.ratio_food = ratio_food




        while running[0]:
            time_delta = clock.tick(config.fps)/1000
            engine.update_food()
            engine.update_all_minos(False)
            if engine.minos_dead == config.nb_minos:
                running[0] = False

        df_minos = pd.DataFrame(engine.minos_list_id, columns=["id", "resistance", "vitesse", "satiete", "vision", "time_lived", "food_eaten", "distance_traveled"])
        return (df_minos, engine.food_data)

main_mode_choice()