import pygame
import sys
import draw
import minos
import time
import random
import food
import pygame_menu
import graph
import pandas as pd

pygame.init()

WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("life simulation")

print_vision = [False]
nb_minos = [1000]
nb_food = [5]
resistance_mu = [1]
resistance_sigma = [0.1]
vitesse_mu = [5]
vitesse_sigma = [0.6]
satiete_mu = [1]
satiete_sigma = [0.15]
vision_mu = [150]
vision_sigma = [40]

#___________________________________________
#              Ecran démarrage
#___________________________________________
state_menu = True
running = False
show_graph = False
def start():
    global state_menu 
    global running 
    state_menu = False
    running = True


menu = pygame_menu.Menu(
    width=WIDTH,
    height=HEIGHT,
    title="Menu Principal",
    theme=pygame_menu.themes.THEME_DARK
)

menu.add.button("Jouer", start)
menu.add.button("Quitter", pygame_menu.events.EXIT)

menu.add.text_input(
    "nombre minos : ",
    default=str(nb_minos[0]),
    onchange=lambda value: nb_minos.__setitem__(0, int(value)if value else nb_minos)
)

menu.add.text_input(
    "nombre food : ",
    default=str(nb_food[0]),
    onchange=lambda value: nb_food.__setitem__(0, int(value)if value else nb_food)
)


menu.add.toggle_switch(
    title="Afficher vision :",
    default=False,
    # Correct : n'attend qu'un seul argument (value)
    onchange=lambda value: print_vision.__setitem__(0, value),
    width=60
)

menu.add.text_input(
    "Resistance µ : ", 
    default=str(resistance_mu[0]), 
    # Si 'val' est vide, on utilise la valeur actuelle de resistance_mu[0]. Sinon, on convertit l'entrée en float.
    onchange=lambda val: resistance_mu.__setitem__(0, float(val) if val else resistance_mu[0])
)
menu.add.text_input(
    "Resistance σ : ", 
    default=str(resistance_sigma[0]), 
    onchange=lambda val: resistance_sigma.__setitem__(0, float(val) if val else resistance_sigma[0])
)
menu.add.text_input(
    "Vitesse µ : ", 
    default=str(vitesse_mu[0]), 
    onchange=lambda val: vitesse_mu.__setitem__(0, float(val) if val else vitesse_mu[0])
)
menu.add.text_input(
    "Vitesse σ : ", 
    default=str(vitesse_sigma[0]), 
    onchange=lambda val: vitesse_sigma.__setitem__(0, float(val) if val else vitesse_sigma[0])
)
menu.add.text_input(
    "Satiété µ : ", 
    default=str(satiete_mu[0]), 
    onchange=lambda val: satiete_mu.__setitem__(0, float(val) if val else satiete_mu[0])
)
menu.add.text_input(
    "Satiété σ : ", 
    default=str(satiete_sigma[0]), 
    onchange=lambda val: satiete_sigma.__setitem__(0, float(val) if val else satiete_sigma[0])
)
menu.add.text_input(
    "Vision µ : ", 
    default=str(vision_mu[0]), 
    onchange=lambda val: vision_mu.__setitem__(0, float(val) if val else vision_mu[0])
)
menu.add.text_input(
    "Vision σ : ", 
    default=str(vision_sigma[0]), 
    onchange=lambda val: vision_sigma.__setitem__(0, float(val) if val else vision_sigma[0])
)



#___________________________________________
#                 Le jeu
#___________________________________________


#Listes pour faire les stats (actualisés à chaque frame)
minos_list_id = [] #Stocke les id et les attributs naturels de chaque mino
minos_list_faim = [] #Stocke la satiete de chaque mino
frame_list = []


while state_menu:
    screen.fill((0,0,0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            state_menu = False

    menu.update(events)
    menu.draw(screen)
    pygame.display.flip()


food_list = []
if (len(food_list)<nb_food[0]):
        food_list.append(food.Food(random.randint(0, WIDTH), random.randint(0,HEIGHT)))
#Initiation de draw : 
d = draw.Draw(screen, WIDTH, HEIGHT)
minos_list = []
for i in range(nb_minos[0]):
        m = minos.Mino(i,0,WIDTH, 0, HEIGHT, food_list,resistance_mu[0], resistance_sigma[0], vitesse_mu[0], vitesse_sigma[0], satiete_mu[0], satiete_sigma[0], vision_mu[0], vision_sigma[0])
        m.draw_vision = print_vision[0]
        minos_list_id.append([i, m.resistance, m.vitesse, m.satiete, m.vision])
        minos_list_faim.append([m.jauge_faim])
        minos_list.append(m)
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_graph = True
            running = False

    
    for mino in minos_list:
        mino.update()
        d.draw_mino(mino)
        
        minos_list_faim[mino.id].append(mino.jauge_faim)
        for f in food_list:
            if f.to_destroy:
                food_list.remove(f)
                del f
    
    if (len(food_list)<nb_food[0]):
        food_list.append(food.Food(random.randint(0, WIDTH), random.randint(0,HEIGHT)))
    
    d.print_background()
    
    d.draw_all_mino(minos_list)
    d.draw_all_food(food_list)

    d.refresh()
    time.sleep(0.05)

menu_graph = pygame_menu.Menu(
    width=WIDTH,
    height=HEIGHT,
    title="Menu Graphiques",
    theme=pygame_menu.themes.THEME_DARK
)

menu_graph.add.label("menu graph titre")

df = pd.DataFrame(minos_list_id, columns=["id", "resistance", "vitesse", "satiete", "vision"])
graph.print_graph_stat_repartition(df["resistance"], df["vitesse"], df["satiete"], df["vision"])
while show_graph:
    screen.fill((0,0,0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            show_graph = False

    menu_graph.update(events)
    menu_graph.draw(screen)
    pygame.display.flip()


pygame.quit()
sys.exit()