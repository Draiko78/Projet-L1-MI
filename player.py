import pygame 

class Player:
    def __init__(self):
        self.image = pygame.image.load("inserer le chemin pour l'image")
        self.body = self.image.get_rect()
