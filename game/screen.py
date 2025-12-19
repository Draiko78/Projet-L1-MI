import pygame
import asyncio
from time import sleep
from player import Player
from animals import Animal
from map_grid import *
from sqlDB import *
from inputPlayer import *
from capteurs.lightS import lightSensor

eventSpawnA = pygame.USEREVENT+1
eventMoveA = pygame.USEREVENT+2
eventLight = pygame.USEREVENT+3

class Screen:
    def __init__(self, pseudo, fullscreen=True):
        self.pseudo = pseudo
        init_db()
        self.saved_salads = get_plants_dict(self.pseudo)
        update_map_with_plants(self.saved_salads)
        self.screen = pygame.display.set_mode((1920,1080))
        if fullscreen:
            pygame.display.toggle_fullscreen()
        self.run = True
        self.sMatrix = []
        self.sDict = {}
        self.player = Player()
        self.animal = None
        self.animal_presence = False
        self.timerSpawnA = pygame.time.set_timer(eventSpawnA, 20000)
        self.timerMoveA = None
        self.background=pygame.image.load("game/assets/background.png")
        self.font = pygame.font.Font('game/Font/pokemon-ds-font.ttf', 72)
        self.text = None
        self.text_rect = None
        self.timerLight = pygame.time.set_timer(eventLight, 500)
        self.light = 600
        self.sun = True
        self.sky = pygame.Surface((1920, 1080))
        self.sky.set_alpha(128)
        self.img_trou = pygame.transform.scale(pygame.image.load("game/assets/trou_sol.png"), (40, 80))
        self.img_graine = pygame.transform.scale(pygame.image.load("game/assets/plante_debut.png"), (40, 80))
        self.img_salade = pygame.transform.scale(pygame.image.load("game/assets/salade.png"), (40, 80))
        self.lose = False
        
    def maj_map(self):
        """Affichage des plantes"""
        for i, j in enumerate(gmap):
            for x, y in enumerate(j):
                pos = ((x - 1) * 40, i * 40)
                if y == 3:
                    self.screen.blit(self.img_trou, pos)
                elif y == 4:
                    self.screen.blit(self.img_graine, pos)
                elif y == 5:
                    self.screen.blit(self.img_salade, pos)

    async def start(self):
        """Boucle principale qui permet de faire fonctionner le jeu"""
        try:
            while self.run:
                
                self.screen.blit(self.background, (0, 0))
                self.maj_map()
                self.screen.blit(self.player.image,dest=self.player.body)
                if self.animal_presence:
                    pygame.draw.rect(self.screen, (255, 0, 0), self.animal.body, 2)
                    self.screen.blit(self.animal.sprite, self.animal.body)
                if self.light < 350:
                    self.screen.blit(self.sky, (0, 0))
                    self.sun = False
                if self.light > 350:
                    self.sun = True
                
                if self.animal_presence:
                    if scream(self.player, self.animal) == 'appeuré':
                        self.animal = None
                        self.animal_presence = False
                        self.timerMoveA = None
                        self.timerSpawnA = pygame.time.set_timer(eventSpawnA, 20000)
                        self.text = None
                        self.text_rect = None
                
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
                            self.lose = True
                            self.screen.blit(self.text, self.text_rect)
                            pygame.display.update()
                            sleep(5)
                            self.run = res[1]
                    if event.type == eventLight:
                        self.light = lightSensor()
                
                plant = plantation(gmap, self.player, self.sun)
                if plant[0]:
                    self.sMatrix.append(plant[1])
                
                if self.text is not None:
                    self.screen.blit(self.text, self.text_rect)
                        
                movement(self.player, gmap)
                
                pygame.draw.rect(self.screen, (255, 0, 0), self.player.body, 2)
                
                await asyncio.sleep(0)
                    
                pygame.display.update()
                
        except asyncio.CancelledError:
            print("Game loop cancelled")
        finally:
            print("Saving game state...")
            try:
                plants_dict = extract_plants_from_map(self.lose)
                save_game_data(self.pseudo, plants_dict, [0])
                print("Game saved from screen class")
            except Exception as e:
                print(f"Error saving in screen: {e}")
