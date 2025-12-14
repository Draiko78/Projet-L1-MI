import pygame
from player import Player
from animals import Animal
from map_grid import gmap
from inputPlayer import movement, scream

eventMoveA = pygame.USEREVENT+1

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920,1080))
        pygame.display.toggle_fullscreen()
        self.run = True
        self.sMatrix = [(120, 200)]
        self.player = Player()
        self.animal = Animal(self.sMatrix)
        self.animal_presence = True
        self.timer = pygame.time.set_timer(eventMoveA, self.animal.speed)
        self.background=pygame.image.load("resized_image.png")

    def start(self):
        while self.run:
            
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image,dest=self.player.body)
            if self.animal_presence:
                self.screen.blit(self.animal.sprite,dest=self.animal.body)
            
            if self.animal_presence:
                if scream(self.player, self.animal) == 'appeuré':
                    self.animal = None
                    self.animal_presence = False
                    self.timer = None
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.run = False
                if self.animal_presence and event.type == eventMoveA:
                    self.animal.moveToSalad(gmap)
                    
            movement(self.player, gmap)
                
            pygame.display.update()
