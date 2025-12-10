import pygame
from grid import set_grid
from player import Player
from map import gmap

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920,1080))
        pygame.display.toggle_fullscreen()
        self.run = True
        self.player = Player()
        self.background=pygame.image.load("resized_image.png")

    def start(self):
        
        while self.run:
                
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image,dest=self.player.body)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    my = self.player.body.left//40
                    mx = self.player.body.top//40
                    if event.key == pygame.K_RIGHT and gmap[mx][my+1] == 0:
                        self.player.body.left+=40
                        self.player.image=self.player.image_droite
                    if event.key == pygame.K_LEFT and gmap[mx][my-1] == 0: 
                        self.player.body.left-=40
                        self.player.image=self.player.image_gauche
                    if event.key == pygame.K_UP and gmap[mx-1][my] == 0:
                        self.player.body.top-=40
                        self.player.image=self.player.image_dos
                    if event.key == pygame.K_DOWN and gmap[mx+1][my] == 0:
                        self.player.body.top+=40
                        self.player.image=self.player.image_face
                if event.type == pygame.QUIT:
                    self.run = False
                
                
                    
                pygame.display.update()
