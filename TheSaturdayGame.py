import pygame
import sys
import random

from pygame.locals import *

black = pygame.Color(0, 0, 0)         # Black
white = pygame.Color(255, 255, 255)   # White
grey = pygame.Color(128, 128, 128)   # Grey 
red = pygame.Color(255, 0, 0)       # Red
green = pygame.Color(1, 50, 32)       # Red

width = 500
height = 600
FPS_limit = 60

villan_count = 5
pygame.init()

display = pygame.display.set_mode((width,height))
pygame.display.set_caption("ThE SaTuRdAy GaMe")
fps = pygame.time.Clock()

class displayScore():
    def __init__(self):
        self.score_str = "Score : "
        self.font  = pygame.font.Font('FreeSansBold.ttf',20)
        self.text = self.font.render(self.score_str+str(0),True,black,grey)
        self.textRect = self.text.get_rect()
        self.textRect.center = (width/2,20)

    def update(self,score):
        self.text = self.font.render(self.score_str+str(score),True,black,grey)

    def draw(self, display):         
        display.blit(self.text,self.textRect)


class villan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(0,0,20,50)
        self.rect.center = (random.randint(40,width-40),30)
        self.score=0

    def move(self):
        self.rect.move_ip(0,random.randint(1,10))
        if(self.rect.bottom > height):
            self.rect.top = 0
            self.score = self.score + 1
            self.rect.center = (random.randint(40,width-40),0)
        return self.score
    
    def draw(self,display):
        pygame.draw.rect(display,red,self.rect)


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(0,0,20,50)
        self.rect.center = (width/2,height-50)

    def draw(self,display):
        pygame.draw.rect(display,green,self.rect)

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if self.rect.left > 0:
            if keys_pressed[K_LEFT]:
                self.rect.move_ip(-5,0)
        if self.rect.right > 0:
            if keys_pressed[K_RIGHT]:
                self.rect.move_ip(5,0)
                    
class game():
    def __init__(self,villan_count):
        self.villan_count = villan_count
        self.villans = []
        for i in range(1,self.villan_count):
            self.villans.append(villan())
        self.P = player()
        self.Ds = displayScore()
        self.flag = True

    def  destroy_objs(self):
        del self.P
        del self.Ds
        for v in self.villans:
            del v
        self.villans = []
    
    def create_objs(self):
        for i in range(1,self.villan_count):
            self.villans.append(villan())
        self.P = player()
        self.Ds = displayScore()
        self.flag = True

def main():
    new_game = game(5)

    while True:
        display.fill(grey)
        
        for event in pygame.event.get():
                if event.type == QUIT: # imported from pygame.locals
                    pygame.quit()
                    sys.exit()

        if new_game.flag ==True:
            score =0 
            for v in new_game.villans:
                score = score + v.move()
            new_game.P.update()
            new_game.Ds.update(score)
        
            for v in new_game.villans:
                v.draw(display)
            new_game.P.draw(display)
            new_game.Ds.draw(display)

            fps.tick(FPS_limit)
        
            for v in new_game.villans:
                v.move()
                if v.rect.colliderect(new_game.P.rect):
                        new_game.flag = False
                        break

        if new_game.flag == False:
            new_game.Ds.draw(display)
            for v in new_game.villans:
                v.draw(display)
            new_game.P.draw(display)
            new_game.Ds.draw(display)
            font  = pygame.font.Font('FreeSansBold.ttf',20)
            text = font.render("To Play Again Press P \n To Quit press Q",True,green,grey)
            textRect = text.get_rect()
            textRect.center = (width/2,height/2)    
            display.blit(text,textRect)         

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_q]:
                pygame.quit()
                sys.exit()
            if keys_pressed[K_p]:
                new_game.destroy_objs()
                new_game.create_objs()
                new_game.flag=True                
        
        pygame.display.update()

if __name__ == "__main__":
   main()