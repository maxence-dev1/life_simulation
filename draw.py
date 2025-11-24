import pygame

class Draw():
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.background = pygame.image.load("fond.png").convert()
    
    def fill_screen(self, new_color = (255,255,255)):
        self.screen.fill(new_color)
    
    def print_background(self):
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen.blit(self.background, (0,0))
        