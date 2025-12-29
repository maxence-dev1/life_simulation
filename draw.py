import pygame
import minos
import food

class Draw():
    """Sert à gérer tout l'affichage"""
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.background = pygame.image.load("fond.png").convert()
    
    def fill_screen(self, new_color = (255,255,255)):
        """Rempli l'écran d'une certaine couleur"""
        self.screen.fill(new_color)
    
    def print_background(self):
        """Affiche le fond en entier"""
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen.blit(self.background, (0,0))
        #pygame.display.flip()
    
    def print_background_zone(self):
        """Affiche une partie du fond"""
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen.blit(self.background, (0,0))

    def refresh(self):
        """Actualise l'écran"""
        pygame.display.flip()
    
    def refresh_zone(self, x, y, width, height):
        """Actualise une certaine zone de l'écran"""
        pygame.display.update((x,y,width, height))

    def draw_mino(self, mino):
        """Affiche un mino"""
        if not mino.to_clear : 
            pygame.draw.rect(self.screen, mino.color, (mino.x, mino.y, mino.width, mino.height), border_radius=5)
            pygame.draw.rect(self.screen, mino.border_color, (mino.x, mino.y, mino.width, mino.height), int(mino.width/15), border_radius=5)
            if mino.draw_vision and not mino.mort : 
                pygame.draw.circle(self.screen, "grey", (mino.middle_x, mino.middle_y), mino.vision, 1)

    def draw_all_mino(self, liste_minos):
        """affiche tous les minos"""
        for m in liste_minos:
            self.draw_mino(m)
            #self.refresh_zone(m.x - m.vitesse, m.y - m.vitesse, m.width + m.vitesse*3, m.height +m.vitesse*3)

    def draw_food(self, food):
        """Affiche une nourriture"""
        pygame.draw.circle(self.screen, food.color, (food.x, food.y), food.size)

    def draw_all_food(self, food):
        """Affiche toutes les nourritures"""
        for f in food:
            self.draw_food(f)
            #self.refresh_zone(f.x -30, f.y-30, 65,65)
    
    def draw_abundance_zone(self, abundance_zone):
        pygame.draw.rect(self.screen, (255,0,0), abundance_zone, 5)

            



        