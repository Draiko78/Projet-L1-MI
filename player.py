import pygame 

class Player:
    def __init__(self):
        self.image = pygame.image.load("perso_face_fin.png")
        self.image = pygame.transform.scale(self.image, (64, 100))
        self.body = self.image.get_rect()
