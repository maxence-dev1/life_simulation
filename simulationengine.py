import pygame, pygame_gui, pygame_menu, numpy, food, random, minos, math


class Engine():
    def __init__(self, width, height, ratio_food, running, d, multiple_mode = False, screen = None, manager = None, use_abundance_zone = False):
        self.d = d
        if not multiple_mode:  
            self.screen = screen
            self.manager = manager
            pygame.display.set_caption("Minos")
            pygame.event.pump()
        self.clock = pygame.time.Clock()
        self.running = running
        self.food_data = []
        self.frame_list = []
        self.width_square = 100
        self.heigh_square = 100
        self.width = width
        self.height = height
        self.ratio_food = ratio_food
        self.nb_food = 0

        self.multiple_mode = multiple_mode
        self.nb_col = math.ceil(self.width / self.width_square)
        self.nb_row = math.ceil(self.height / self.heigh_square)
        self.grid = numpy.empty((self.nb_row,self.nb_col), dtype=object)
        self.food_list = []
        self.minos_list = []
        self.nb_frame = 0
        self.old_nb_frame = 0 
        self.minos_dead = 0
        self.minos_list_id = []
        self.nb_minos = 0
        self.size_food = 0
        
        self.use_abundance_zone = use_abundance_zone
        self.abundance_zone = [0,0,0,0]
        self.time_next_move_abundance_zone = 0

        self.compteur_ajouter_food = 0
        



    def init_grid(self):
        for i in range(self.nb_row):
            for j in range(self.nb_col):
                self.grid[i,j] = []    


    def init_food_list(self):
        surface = self.width* self.height
        densite = self.nb_minos/surface
        self.size_food = int(max(1, min(10,0.5/(densite**0.25))))
        for i in range(int(self.nb_minos*self.ratio_food)):
            self.food_list.append(food.Food(random.randint(10, self.width-10), random.randint(10,self.height-10), self.size_food ))

    def init_gui(self, label):   
        if not self.multiple_mode:
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

    def init_minos(self, nb_minos,  resistance_mu, resistance_sigma, vitesse_mu, vitesse_sigma, satiete_mu, satiete_sigma, vision_mu, vision_sigma, print_vision):
        self.nb_minos = nb_minos
        self.nb_food = self.ratio_food*self.nb_minos
        self.minos_list_id = numpy.zeros((nb_minos,8), dtype=numpy.float64) #Stocke les id et les attributs naturels de chaque mino
        surface = self.width* self.height
        densite = nb_minos/surface
        size = int(max(8,50 / (1 + 2400 * densite)))

        for i in range(nb_minos):
                m = minos.Mino(i,size, 0,self.width, 0, self.height, self.food_list, resistance_mu, resistance_sigma, vitesse_mu, vitesse_sigma, satiete_mu, satiete_sigma, vision_mu, vision_sigma)
                m.draw_vision = print_vision
                self.minos_list_id[i,0] = i
                self.minos_list_id[i,1] = m.resistance
                self.minos_list_id[i,2] = m.vitesse
                self.minos_list_id[i,3] = m.satiete
                self.minos_list_id[i,4] = m.vision
                self.minos_list_id[i,5] = 0
                self.minos_list_id[i,5] = 0
                self.minos_list_id[i,5] = 0
                self.food_data.append([m.jauge_faim])
                self.minos_list.append(m)
    
    def init_abundance_zone(self):
        self.abundance_zone = [random.randint(0,self.width - 300), random.randint(0,self.height-300), 300, 300]
        self.time_next_move_abundance_zone = random.randint(70, 250)

    def update_abundance_zone(self):
        if self.nb_frame == self.time_next_move_abundance_zone:
            for f in self.food_list:
                if  self.abundance_zone[0] <= f.x <= self.abundance_zone[0] + self.abundance_zone[2] and self.abundance_zone[1] <= f.y <= self.abundance_zone[1] + self.abundance_zone[3]:
                    f.to_destroy = True
            new_width = random.randint(200,400)
            new_height = random.randint(200,400)
            self.abundance_zone = [random.randint(0,self.width - new_width), random.randint(0,self.height-new_height), new_width, new_height]
            self.time_next_move_abundance_zone = self.nb_frame + random.randint(70, 250)
            

    def draw_abundance_zone(self):
        self.d.draw_abundance_zone(self.abundance_zone)


    def update_food(self):
        self.nb_frame+=1
         #print("nb minos en vie : ", self.nb_minos - self.minos_dead, "nb food : ", self.nb_food)
        if self.nb_frame >= self.old_nb_frame + 50:
         self.nb_food =(self.nb_minos - self.minos_dead)*self.ratio_food
         self.old_nb_frame = self.nb_frame  

        for ligne in self.grid:
            for cellule_liste in ligne:
                cellule_liste.clear()
        self.food_list = [f for f in self.food_list if not f.to_destroy]
        i=0
        if self.use_abundance_zone:
            while (len(self.food_list)<self.nb_food):
                
                if self.compteur_ajouter_food %4 != 0:
                    f = food.Food(random.randint(10, self.width-10), random.randint(10,self.height-10), self.size_food )
                    self.food_list.append(f)
                else : 
                    f = food.Food(random.randint(self.abundance_zone[0], self.abundance_zone[0] + self.abundance_zone[2]), random.randint(self.abundance_zone[1],self.abundance_zone[1] + self.abundance_zone[3]), self.size_food, True)
                    if random.randint(1,3)%3 != 0:
                        f.color = (239,191,4)
                        f.valeur = 35
                    self.food_list.append(f)
                self.compteur_ajouter_food +=1
                if i >= 5:
                    break
                i+=1
        else : 
            while (len(self.food_list)<self.nb_food):
                f = food.Food(random.randint(10, self.width-10), random.randint(10,self.height-10), self.size_food )
                self.food_list.append(f)
                self.compteur_ajouter_food +=1
                if i >= 5:
                    break
                i+=1

        for f in self.food_list: #On construit la grille
            self.grid[f.y//100, f.x//100].append(f)

    def update_all_minos(self, afficher_jeu):
        self.minos_dead = 0
        food_in_abundance = [f for f in self.food_list if 
                     self.abundance_zone[0] <= f.x <= self.abundance_zone[0] + self.abundance_zone[2] and 
                     self.abundance_zone[1] <= f.y <= self.abundance_zone[1] + self.abundance_zone[3]]
        for mino in self.minos_list:
            if self.abundance_zone[0] <= mino.x <= self.abundance_zone[0] + self.abundance_zone[2] and self.abundance_zone[1] <= mino.y <= self.abundance_zone[1] + self.abundance_zone[3]:
                mino.nb_time_in_abundance_zone +=1
            if mino.mort:
                self.minos_list_id[mino.id,6] = mino.food_eaten
                self.minos_list_id[mino.id,7] = mino.distance_traveled
                self.minos_list_id[mino.id,5] = mino.time_lived
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
            food_list_to_see_collisions = list(food_in_abundance)
            for ligne, colonne in cases_chevauchée:
                if 0 <= ligne < self.grid.shape[0] and 0 <= colonne < self.grid.shape[1]:
                    food_list_to_see_collisions.extend(self.grid[int(ligne), int(colonne)])
            if afficher_jeu:
                self.d.draw_mino(mino)
                #Mtn il faut trouver quel(s) cases envoyer au minos
                mino.update(self.nb_frame, self.food_list, food_list_to_see_collisions)
            else : 
                mino.update_speed(self.nb_frame, self.food_list, food_list_to_see_collisions) 
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