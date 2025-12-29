import random


class Food():
    def __init__(self, x,y, size, in_zone = False):
        self.in_zone = in_zone
        self.x = x
        self.y = y
        self.size = size
        self.to_destroy = False
        if random.randint(1,15)%15 == 0:
            self.color = (239,191,4)
            self.valeur = 35
        else :
            self.color = (0,0,255)
            self.valeur = 25

        