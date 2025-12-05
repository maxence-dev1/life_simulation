import pygame, sys, draw, minos, time, random, food, pygame_menu, graph, pygame_gui, numpy
import pandas as pd
#5000 minos avec 0 food avant opti : afficher->1.13 sans afficher -> 9 sec
#1000 minos avec 500 food avant opti : afficher->4.07 sans afficher -> 2.46 min


pygame.init()

WIDTH = 2000
HEIGHT = 1000

WIDTH_SQUARE = 100
HEIGHT_SQUARE = 100

grille = numpy.empty((10,20), dtype=object) #La grille qui contiendra la nourriture
for i in range(10):
    for j in range(20):
         grille[i,j] = []


#Tracer grille
# for i in range(20):
#             for j in range(10):
#                  pygame.draw.line(screen, (255,0,255), (i*100, j*100), ((i*100+100, j*100)))
#                  pygame.draw.line(screen, (255,0,255), (i*100, j*100), ((i*100, j*100+100)))
#                  pygame.draw.line(screen, (255,0,255), (i*100+100, j*100), ((i*100+100, j*100+100)))
#                  pygame.draw.line(screen, (255,0,255), (i*100, j*100+100), ((i*100+100, j*100+100)))
#                  pygame.display.flip()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH,HEIGHT), theme_path='theme.json')
clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption("life simulation")
pygame.event.pump()

print_vision = [False]
afficher_jeu = [True]
nb_minos = [10]
nb_food = [3]
resistance_mu = [2]
resistance_sigma = [0.5]
vitesse_mu = [5]
vitesse_sigma = [1.5]
satiete_mu = [1]
satiete_sigma = [0.75]
vision_mu = [150]
vision_sigma = [120]

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

menu.add.toggle_switch(
    title="Afficher jeu (beaucoup moins de temps de simulation) :",
    default=True,
    # Correct : n'attend qu'un seul argument (value)
    onchange=lambda value: afficher_jeu.__setitem__(0, value),
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



#_______________________________________________________________________________________________________________________
#                 Le jeu
#_______________________________________________________________________________________________________________________


#Listes pour faire les stats (actualisés à chaque frame)

minos_list_faim = [] #Stocke la satiete de chaque mino
frame_list = []

import pygame
import pygame_gui

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
    text=f"FPS : {clock.get_fps():.1f}/{fps}", 
    manager=manager,
    container=frame_fps
)

button_more_fps = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(160, 15, 35, 30),
    text="+",
    manager=manager,
    container=frame_fps
)

def more_fps():
    global fps
    fps += 1

def less_fps():
    global fps
    fps -= 1




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
if (len(food_list)<nb_food[0] ):
        food_list.append(food.Food(random.randint(0, WIDTH-10), random.randint(0,HEIGHT-10)))
#Initiation de draw : 
d = draw.Draw(screen, WIDTH, HEIGHT)
minos_list = []


minos_list_id = numpy.zeros((nb_minos[0],6), dtype=numpy.float64) #Stocke les id et les attributs naturels de chaque mino
for i in range(nb_minos[0]-1):
        m = minos.Mino(i,0,WIDTH, 0, HEIGHT, food_list,resistance_mu[0], resistance_sigma[0], vitesse_mu[0], vitesse_sigma[0], satiete_mu[0], satiete_sigma[0], vision_mu[0], vision_sigma[0])
        m.draw_vision = print_vision[0]
        minos_list_id[i,0] = i
        minos_list_id[i,1] = m.resistance
        minos_list_id[i,2] = m.vitesse
        minos_list_id[i,3] = m.satiete
        minos_list_id[i,4] = m.vision
        minos_list_id[i,5] = 0
        minos_list_faim.append([m.jauge_faim])
        minos_list.append(m)

text_pas_affichage = pygame.font.Font(None, 36).render("Simulation en cours, veuillez patienter", True, "white")
one = True
nb_frame = 0
old_nb_frame = 0


while running:
    #print(len(food_list))
    time_delta = clock.tick(fps)/1000
    nb_frame+=1
    if nb_frame >= old_nb_frame + 50 and nb_food[0]>5 :
         nb_food[0]*=0.90
         old_nb_frame = nb_frame    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                  running = False
        manager.process_events(event)
        if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == button_more_fps):
            more_fps()
        elif (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == button_less_fps):
                less_fps()

    #Je garde food_list mais je ne gere pas les collisions avec
    for ligne in grille:
        for cellule_liste in ligne:
            cellule_liste.clear()
    food_list = [f for f in food_list if not f.to_destroy]
    while (len(food_list)<nb_food[0]):
        food_list.append(food.Food(random.randint(0, WIDTH-10), random.randint(0,HEIGHT-10)))

    for f in food_list: #On construit la grille
        grille[f.y//100, f.x//100].append(f)

    minos_dead = 0
    for mino in minos_list:
        if mino.mort:
             minos_dead+=1
        cases_chevauchée = []
        nw = (mino.y//100, mino.x//100)
        if (nw not in cases_chevauchée):
            cases_chevauchée.append(nw)
        ne = ((mino.y + mino.width)//100, (mino.x)//100)
        if (ne not in cases_chevauchée):
            cases_chevauchée.append(ne)
        sw = (mino.y//100, (mino.x+mino.height)//100)
        if (sw not in cases_chevauchée):
            cases_chevauchée.append(sw)
        se = ((mino.y+ mino.width)//100, (mino.x+mino.height)//100)
        if (se not in cases_chevauchée):
            cases_chevauchée.append(se)
        food_list_to_see_collisions = []
        for ligne, colonne in cases_chevauchée:
            if 0 <= ligne < grille.shape[0] and 0 <= colonne < grille.shape[1]:
                food_list_to_see_collisions.append(grille[int(ligne), int(colonne)])
        food_neighbors_flat = [f for sublist in food_list_to_see_collisions for f in sublist]
        if afficher_jeu[0]:
            d.draw_mino(mino)
            #Mtn il faut trouver quel(s) cases envoyer au minos
                
            mino.update(nb_frame, food_list, food_neighbors_flat)
        else : 
             mino.update_speed(nb_frame, food_list, food_list_to_see_collisions)
        minos_list_id[mino.id,5] = mino.time_lived
        minos_list_faim[mino.id].append(mino.jauge_faim)
        
    
    print("minos morts : ", minos_dead,"/", nb_minos[0]-1)
    if minos_dead == nb_minos[0]-1:
         running = False
    if afficher_jeu[0]:
        d.print_background()
        # for i in range(20):
        #      for j in range(10):
        #           pygame.draw.line(screen, (255,0,255), (i*100, j*100), ((i*100+100, j*100)))
        #           pygame.draw.line(screen, (255,0,255), (i*100, j*100), ((i*100, j*100+100)))
        #           pygame.draw.line(screen, (255,0,255), (i*100+100, j*100), ((i*100+100, j*100+100)))
        #           pygame.draw.line(screen, (255,0,255), (i*100, j*100+100), ((i*100+100, j*100+100)))
        d.draw_all_mino(minos_list)
        d.draw_all_food(food_list)
        manager.update(time_delta)
        manager.draw_ui(screen)
        label_fps.set_text(f"FPS : {clock.get_fps():.1f}/{fps}")
        d.refresh()
    
        
    else : 
        d.fill_screen((0,0,0))
        screen.blit(text_pas_affichage, (100,200))
        if one: 
             pygame.display.flip()
             one = False



def normaliser(x,minimum,maximum):
     return (x-minimum)/(maximum - minimum)



df = pd.DataFrame(minos_list_id, columns=["id", "resistance", "vitesse", "satiete", "vision", "temps vécu"])
print(df)

a = min(df["resistance"])
b = max(df["resistance"])
df["resistance_normee"] = df["resistance"].apply(lambda x: normaliser(x, a, b))
a = min(df["vitesse"])
b = max(df["vitesse"])
df["vitesse_normee"] = df["vitesse"].apply(lambda x: normaliser(x, a, b))
a = min(df["satiete"])
b = max(df["satiete"])
df["satiete_normee"] = df["satiete"].apply(lambda x: normaliser(x, a, b))
a = min(df["vision"])
b = max(df["vision"])
df["vision_normee"] = df["vision"].apply(lambda x: normaliser(x, a, b))

graph.menu_statistique(df, minos_list_faim)


pygame.quit()
sys.exit()