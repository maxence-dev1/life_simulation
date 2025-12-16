import pygame, pygame_gui, pygame_menu, numpy, food, random, minos


class Engine():
    def __init__(self, width, height, nb_food, running, d):
        self.d = d
        self.screen = pygame.display.set_mode((width, height))
        self.manager = pygame_gui.UIManager((width,height), theme_path='theme.json')
        self.clock = pygame.time.Clock()
        self.running = running
        self.food_data = []
        self.frame_list = []
        self.width_square = 100
        self.heigh_square = 100
        self.width = width
        self.height = height
        self.nb_food = nb_food
        self.nb_col = int(self.width / self.width_square)
        self.nb_row = int(self.height / self.heigh_square)
        self.grid = numpy.empty((self.nb_row,self.nb_col), dtype=object)
        self.food_list = []
        self.minos_list = []
        self.nb_frame = 0
        self.old_nb_frame = 0 
        self.minos_dead = 0
        self.minos_list_id = []
        self.nb_minos = 0



        pygame.display.set_caption("Minos")
        pygame.event.pump()



    def init_grid(self):
        for i in range(self.nb_row):
            for j in range(self.nb_col):
                self.grid[i,j] = []    

    def init_food_list(self):
        if (len(self.food_list)<self.nb_food ):
            self.food_list.append(food.Food(random.randint(0, self.width-10), random.randint(0,self.height-10)))

    def init_gui(self, label):   
        self.frame_fps = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 210, 60), 
            manager=self.manager,
        )

        self.button_less_fps = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(5, 15, 35, 30),
            text="-",
            manager=self.manager,
            container=self.frame_fps
        )


        self.label_fps = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 15, 90, 30),
            text=label, 
            manager=self.manager,
            container=self.frame_fps
        )

        self.button_more_fps = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(160, 15, 35, 30),
            text="+",
            manager=self.manager,
            container=self.frame_fps
        )

    def init_minos(self, nb_minos, size_minos,  resistance_mu, resistance_sigma, vitesse_mu, vitesse_sigma, satiete_mu, satiete_sigma, vision_mu, vision_sigma, print_vision):
        self.minos_list_id = numpy.zeros((nb_minos,6), dtype=numpy.float64) #Stocke les id et les attributs naturels de chaque mino
        for i in range(nb_minos-1):
                m = minos.Mino(i,size_minos, 0,self.width, 0, self.height, self.food_list,resistance_mu, resistance_sigma, vitesse_mu, vitesse_sigma, satiete_mu, satiete_sigma, vision_mu, vision_sigma)
                m.draw_vision = print_vision
                self.minos_list_id[i,0] = i
                self.minos_list_id[i,1] = m.resistance
                self.minos_list_id[i,2] = m.vitesse
                self.minos_list_id[i,3] = m.satiete
                self.minos_list_id[i,4] = m.vision
                self.minos_list_id[i,5] = 0
                self.food_data.append([m.jauge_faim])
                self.minos_list.append(m)
    

    def update_food(self):
        self.nb_frame+=1
        if self.nb_frame >= self.old_nb_frame + 50 and self.nb_food>1 :
         self.nb_food*=0.90
         self.old_nb_frame = self.nb_frame  

        for ligne in self.grid:
            for cellule_liste in ligne:
                cellule_liste.clear()
        self.food_list = [f for f in self.food_list if not f.to_destroy]
        while (len(self.food_list)<self.nb_food):
            self.food_list.append(food.Food(random.randint(0, self.width-10), random.randint(0,self.height-10)))

        for f in self.food_list: #On construit la grille
            self.grid[f.y//100, f.x//100].append(f)

    def update_all_minos(self, afficher_jeu):
        self.minos_dead = 0
        for mino in self.minos_list:
            if mino.mort:
                self.minos_dead+=1
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
                if 0 <= ligne < self.grid.shape[0] and 0 <= colonne < self.grid.shape[1]:
                    food_list_to_see_collisions.append(self.grid[int(ligne), int(colonne)])
            food_neighbors_flat = [f for sublist in food_list_to_see_collisions for f in sublist]
            if afficher_jeu:
                self.d.draw_mino(mino)
                #Mtn il faut trouver quel(s) cases envoyer au minos
                mino.update(self.nb_frame, self.food_list, food_neighbors_flat)
            else : 
                mino.update_speed(self.nb_frame, self.food_list, food_neighbors_flat)
            self.minos_list_id[mino.id,5] = mino.time_lived
            self.food_data[mino.id].append(mino.jauge_faim)


    def print_grid(self, print_grille):
        self.d.print_background()
        if print_grille:
             for i in range(self.nb_col):
                  for j in range(self.nb_row):
                       pygame.draw.line(self.screen, (255,0,255), (i*100, j*100), ((i*100+100, j*100)))
                       pygame.draw.line(self.screen, (255,0,255), (i*100, j*100), ((i*100, j*100+100)))
                       pygame.draw.line(self.screen, (255,0,255), (i*100+100, j*100), ((i*100+100, j*100+100)))
                       pygame.draw.line(self.screen, (255,0,255), (i*100, j*100+100), ((i*100+100, j*100+100)))