import pygame

pygame.init()

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((200,400))
        self.run = True

    def start(self):
        
        while self.run:

            for event in pygame.event.get():
                if event == pygame.QUIT:
                    self.run = False

pygame.quit()