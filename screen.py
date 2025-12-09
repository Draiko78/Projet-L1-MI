import pygame
from grid import set_grid
from player import Player

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920,1080))
        pygame.display.toggle_fullscreen()
        self.run = True
        self.player = Player()

    def start(self):
        
        while self.run:
                
            self.screen.fill((0,0,0))
            self.screen.blit(self.player.image, self.player.body)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.player.body.left+40<1920:
                        self.player.body.left+=40
                    if event.key == pygame.K_LEFT and self.player.body.left-40>=0: 
                        self.player.body.left-=40
                        self.player.image=self.player.image_gauche
                    if event.key == pygame.K_UP and self.player.body.top-40>=0:
                        self.player.body.top-=40
                        self.player.image=self.player.image_dos
                    if event.key == pygame.K_DOWN and self.player.body.top+40<1080:
                        self.player.body.top+=40
                        self.player.image=self.player.image_face
                if event.type == pygame.QUIT:
                    self.run = False
                
                
                    
                pygame.display.update()
