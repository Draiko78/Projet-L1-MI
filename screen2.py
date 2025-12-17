import pygame
from time import sleep
from player import Player
from animals import Animal
from map_grid import gmap
from inputPlayer import movement, scream
#from capteurs.lightS import lightSensor
from plante import plantation

eventSpawnA = pygame.USEREVENT+1
eventMoveA = pygame.USEREVENT+2
eventLight = pygame.USEREVENT+3

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920,1080))
        pygame.display.toggle_fullscreen()
        self.run = True
        self.sMatrix = []
        self.player = Player()
        self.animal = None
        self.animal_presence = False
        self.timerSpawnA = pygame.time.set_timer(eventSpawnA, 2000)
        self.timerMoveA = None
        self.background=pygame.image.load("resized_image.png")
        self.font = pygame.font.Font('Font/pokemon-ds-font.ttf', 72)
        self.text = None
        self.text_rect = None
        #self.timerLight = pygame.time.set_timer(eventLight, 500)
        self.light = 600
        self.sky = pygame.Surface((1920, 1080))
        self.sky.set_alpha(128)
        self.img_trou = pygame.transform.scale(pygame.image.load("trou_sol.png"), (40, 80))
        self.img_graine = pygame.transform.scale(pygame.image.load("plante_debut.png"), (40, 80))
        self.img_salade = pygame.transform.scale(pygame.image.load("salade.png"), (40, 80))

    def start(self):
        while self.run:
            
            self.screen.blit(self.background, (0, 0))
            self.maj_map()
            self.screen.blit(self.player.image,dest=self.player.body)
            if self.animal_presence:
                self.screen.blit(self.animal.sprite,dest=self.animal.body)
            if self.light < 350:
                self.screen.blit(self.sky, (0, 0))
            
            if self.animal_presence:
                '''if scream(self.player, self.animal) == 'appeuré':
                    self.animal = None
                    self.animal_presence = False
                    self.timerMoveA = None
                    self.timerSpawnA = pygame.time.set_timer(eventSpawnA, 2000)
                    self.text = None
                    self.text_rect = None'''
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.run = False
                plant = plantation(gmap, self.player, event)
                if plant[0]:
                    self.sMatrix.append(plant[1])
                if not self.animal_presence and event.type == eventSpawnA:
                    if len(self.sMatrix) != 0:
                        self.animal = Animal(self.sMatrix)
                        self.timerMoveA = pygame.time.set_timer(eventMoveA, self.animal.speed)
                        self.animal_presence = True
                        self.timerSpawnA = None
                if self.animal_presence and event.type == eventMoveA:
                    res = self.animal.moveToSalad(gmap, self.font)
                    self.text = res[0]
                    self.text_rect = self.text.get_rect(center=(960, 540))
                    if not res[1]:
                        self.screen.blit(self.text, self.text_rect)
                        pygame.display.update()
                        sleep(5)
                        self.run = res[1]
                #if event.type == eventLight:
                    #self.light = lightSensor()
                
                        
            if self.text is not None:
                self.screen.blit(self.text, self.text_rect)
                    
            movement(self.player, gmap)
                
            pygame.display.update()
    def maj_map(self):
    	for i,j in enumerate(gmap):
    		for x,y in enumerate(j):
    			pos=((x-1)*40,i*40)
    			if y==3:
    				self.screen.blit(self.img_trou,pos)
    			elif y==4:
    				self.screen.blit(self.img_graine,pos)
    			elif y==5:
    				self.screen.blit(self.img_salade,pos)
    
    
