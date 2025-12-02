import random
import math

def dist(x1,y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Mino:
    def __init__(self, id, min_x, max_x, min_y, max_y, food_list, resistance_mu, resistance_sigma, vitesse_mu, vitesse_sigma, satiete_mu, satiete_sigma, vision_mu, vision_sigma):
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
        self.mort = False
        self.to_clear = False
        self.food_list = food_list
        self.destination_food = None
        self.destinationx = None
        self.destinationy = None
        self.find_destination()
        self.draw_vision = True
        self.time_lived = None

        

        self.width = 50
        self.height = 50

        

    
    def update(self, nb_frame):
        """Actualise entierement un mino"""
        if not self.mort : 
            self.time_lived = nb_frame
            self.go_to_destination()
            self.update_jauge_faim()
            self.is_on_food()
        else :
            self.color = ((self.color[0]*0.96,self.color[1]*0.96,self.color[2]*0.96))
            if (self.color[0]<1):
                self.to_clear = True

    def is_on_food(self):
        for f in self.food_list:
            if (self.x<=f.x - 5 <=self.x + self.width or  self.x<=f.x +5 <=self.x + self.width)   and (self.y<=f.y+5<=self.y + self.height or self.y<=f.y -5 <=self.y + self.height) and not f.to_destroy:
                f.to_destroy = True
                if self.jauge_faim + 30*self.satiete <= self.resistance*150:
                    self.jauge_faim += 30*self.satiete

    def update_jauge_faim(self):
        """Actualise la jauge de faim"""
        self.jauge_faim -= 0.5
        if self.jauge_faim <= 0:
            self.mort = True
            
            
        else :
            val = max(0, min(1, self.jauge_faim / 100 * self.resistance))
            self.color = (int(255 * (1 - val)), int(255 * val), 0)

    def find_random_destination(self):
        """Trouve une nouvelle destination aléatoire ou aller"""
        self.destinationx = random.randint(self.min_x, self.max_x)
        self.destinationy = random.randint(self.min_y, self.max_y)


    def get_closer_food(self):
        dist_min = 9999
        x_to_go = None
        for f in self.food_list:
            if not f.to_destroy:
                distance = dist(self.x, self.y, f.x, f.y)
                if distance<dist_min:
                    dist_min = distance
                    x_to_go = f.x
                    y_to_go = f.y
                    food = f
        if x_to_go == None:
            return -1,-1,-1,-1
        return dist_min, x_to_go, y_to_go, food

    def find_destination(self):
        """Trouve une nouvelle destination de nourriture ou aller"""
        dist_min = 9999
        x_to_go = None
        y_to_go = None
        food = None
        _, x_to_go, y_to_go, food = self.get_closer_food()
        if x_to_go== None or self.vision < dist_min :
            self.find_random_destination()
            return
        if x_to_go != -1:
            self.destination_food = food
            self.destinationx = x_to_go
            self.destinationy = y_to_go


    def go_to_destination(self):
        """Avance vers la destination"""
        self.middle_x = self.x + self.width/2
        self.middle_y = self.y + self.height/2
        if self.destinationx-5 <=self.x <= self.destinationx+5 and self.destinationy-5 <= self.y <= self.destinationy+5: #Si il atteind la destination
            if self.destination_food is not None:
                self.destination_food.to_destroy = True
            self.find_destination()
        
        dist,x_to_go,y_to_go,food = self.get_closer_food()
        if (dist<self.vision and x_to_go != -1): #Vérifie toujours qu'il n'y a pas de nourriture plus pret
            self.destinationx = x_to_go
            self.destinationy = y_to_go
            self.destination_food = food


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