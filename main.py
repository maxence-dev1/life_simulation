import pygame
import sys
import draw
import minos
import time
import random
import food

pygame.init()

WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("life simulation")


food_list = []
if (len(food_list)<5):
        food_list.append(food.Food(random.randint(0, WIDTH), random.randint(0,HEIGHT)))
#Initiation de draw : 
d = draw.Draw(screen, WIDTH, HEIGHT)
minos_list = []
for i in range(1):
        m = minos.Mino(0,WIDTH, 0, HEIGHT, food_list)
        minos_list.append(m)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    for mino in minos_list:
        mino.update()
        d.draw_mino(mino)
    for f in food_list:
         if f.to_destroy:
              food_list.remove(f)
              del f
    
    if (len(food_list)<5):
        food_list.append(food.Food(random.randint(0, WIDTH), random.randint(0,HEIGHT)))
    
    d.print_background()
    
    d.draw_all_mino(minos_list)
    d.draw_all_food(food_list)
    
    d.refresh()
    time.sleep(0.05)
    
    


pygame.quit()
sys.exit()