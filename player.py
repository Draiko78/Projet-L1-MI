import pygame 

class Player:
    def __init__(self):
        self.image=pygame.image.load("perso_face_fin.png")
        self.image=pygame.transform.scale(self.image,(64,100))
        
        self.image_face = pygame.image.load("perso_face_fin.png")
        self.image_face = pygame.transform.scale(self.image_face, (64, 100))
        
        self.image_gauche=pygame.image.load("perso_profile_gauche_fin.png")
        self.image_gauche = pygame.transform.scale(self.image_gauche, (64, 100))
        
        self.image_dos=pygame.image.load("perso_dos_fin.png")
        self.image_dos = pygame.transform.scale(self.image_dos, (64, 100))
        
        self.image_droite = pygame.transform.flip(self.image_gauche, True, False)
        
        self.body = self.image.get_rect()
