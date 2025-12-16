import random
import math

def dist(x1,y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Mino:
    def __init__(self, id,size, min_x, max_x, min_y, max_y, food_list, resistance_mu, resistance_sigma, vitesse_mu, vitesse_sigma, satiete_mu, satiete_sigma, vision_mu, vision_sigma):
        self.id = id
        self.resistance = random.gauss(resistance_mu, resistance_sigma)     
        self.vitesse = random.gauss(vitesse_mu, vitesse_sigma) 
        self.satiete = random.gauss(satiete_mu, satiete_sigma)
        self.vision = random.gauss(vision_mu, vision_sigma)
        self.jauge_faim = 100 * self.resistance
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.x = random.randint(min_x, max_x)
        self.y = random.randint(min_y, max_y)
        
        
        self.color = (0 + int(255 * (1 - (1/(1+math.exp(-self.jauge_faim))))),0 + int(255 * ((1/(1+math.exp(-self.jauge_faim))))),0)
        self.border_color = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
        
        self.mort = False
        self.to_clear = False
        self.food_list = []
        self.food_list_to_see_collisions = []
        self.destination_food = None
        self.destinationx = None
        self.destinationy = None
        self.find_destination()
        self.draw_vision = True
        self.time_lived = 0
        
        

        self.width = size
        self.height = size
        self.middle_x = self.x + self.width/2
        self.middle_y = self.y + self.height/2

        self.consommation_fixe = 0.5 

    
    def update(self, nb_frame, food_list, food_list_to_see_collisions):
        """Actualise entierement un mino"""
        if not self.mort : 
            #print(f"food_list : {len(food_list)}, foo_list_to_see_collision : {len(food_list_to_see_collisions)}")
            self.food_list_to_see_collisions = food_list_to_see_collisions
            self.food_list = food_list
            self.time_lived = nb_frame
            self.go_to_destination()
            self.update_jauge_faim()
            self.is_on_food()
        else :
            self.color = ((self.color[0]*0.96,self.color[1]*0.96,self.color[2]*0.96))
            self.border_color = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
            if (self.color[0]<1):
                self.to_clear = True
    
    def update_speed(self, nb_frame, food_list, food_list_to_see_collisions):
        """Actualise un mino sauf les fonctions visuelles"""
        if not self.mort :
            self.food_list_to_see_collisions = food_list_to_see_collisions
            self.food_list = food_list
            self.time_lived = nb_frame
            self.go_to_destination()
            self.update_jauge_faim()
            self.is_on_food()

    def is_on_food(self):
        #On vérifie uniquement les collisions avec les food dont il chevauche les cases
        for f in self.food_list_to_see_collisions:
                if (self.x<=f.x - 5 <=self.x + self.width or  self.x<=f.x +5 <=self.x + self.width)   and (self.y<=f.y+5<=self.y + self.height or self.y<=f.y -5 <=self.y + self.height) and not f.to_destroy:
                    f.to_destroy = True
                    if self.jauge_faim + 30*self.satiete <= self.resistance*150:
                        self.jauge_faim += 30*self.satiete

    def update_jauge_faim(self):
        """Actualise la jauge de faim"""
        self.jauge_faim -= (self.consommation_fixe + self.resistance*0.05 + self.vitesse*0.025 + int(not bool(self.destination_food))*0.25*self.consommation_fixe)
        if self.jauge_faim <= 0:
            self.mort = True         
        else :
            val = max(0, min(1, self.jauge_faim / 100 * self.resistance))
            self.color = (int(255 * (1 - val)), int(255 * val), 0)

    def find_random_destination(self):
        """Trouve une nouvelle destination aléatoire ou aller"""
        self.destination_food = None
        self.destinationx = random.randint(self.min_x, self.max_x)
        self.destinationy = random.randint(self.min_y, self.max_y)


    def get_closer_food(self, list_to_search):
        dist_min = 9999
        x_to_go = None
        for f in list_to_search:
            if not f.to_destroy:
                distance = dist(self.x, self.y, f.x, f.y)
                if distance<dist_min:
                    dist_min = distance
                    x_to_go = f.x
                    y_to_go = f.y
                    food = f
        if x_to_go == None:
            return -1,-1,-1,None
        return dist_min, x_to_go, y_to_go, food


    def find_destination(self, do_random = True):
        """Trouve une nouvelle destination de nourriture ou aller"""
        #On regarde d'abord dans le voisinage
        dist_min_local, x_local, y_local, food_local = self.get_closer_food(self.food_list_to_see_collisions)
        if food_local is not None and dist_min_local <= self.vision:
            self.destination_food = food_local
            self.destinationx = x_local
            self.destinationy = y_local
            return

        #Si il n'y a pas de food dans le voisinage
        dist_min_global, x_global, y_global, food_global = self.get_closer_food(self.food_list)
        if food_global is not None and dist_min_global <= self.vision:
            self.destination_food = food_global
            self.destinationx = x_global
            self.destinationy = y_global
            return
        if do_random:
            self.find_random_destination()


    def go_to_destination(self):
        """Avance vers la destination"""
        self.middle_x = self.x + self.width/2
        self.middle_y = self.y + self.height/2
        if self.destinationx-5 <=self.x <= self.destinationx+5 and self.destinationy-5 <= self.y <= self.destinationy+5: #Si il atteind la destination
            if self.destination_food is not None:
                self.destination_food.to_destroy = True
            self.find_destination()
        else :
            if self.time_lived%10 ==0: #Il vérifie uniquement 1 frame sur 10 car c'est couteux
                self.find_destination(False) # Pour vérifier si il trouve une autre nourriture plus pret

        if self.destinationx-5 <=self.x <= self.destinationx+5 : 
            pass
        elif self.destinationx > self.x:
            self.x += self.vitesse
        else : 
            self.x -= self.vitesse
        
        if self.destinationy-5 <= self.y <= self.destinationy+5: 
            pass
        elif self.destinationy > self.y:
            self.y += self.vitesse
        else : 
            self.y -= self.vitesse