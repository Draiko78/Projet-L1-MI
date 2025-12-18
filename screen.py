import pygame
from time import sleep
from player import Player
from animals import Animal
from map_grid import gmap
from inputPlayer import movement, scream
from capteurs.lightS import lightSensor
import capteurs.grove_button_quit as grove_quit
import math  # AJOUT
import random  # AJOUT

eventSpawnA = pygame.USEREVENT+1
eventMoveA = pygame.USEREVENT+2
eventLight = pygame.USEREVENT+3

grove_quit.quit_button()
# ============ CLASSES POUR LES INDICATEURS (AJOUTER ICI) ============

class IndicateurTemperature:
    """
    Indicateur visuel de température
    Température élevée (>25°C) → orange + message "Il fait chaud"
    """
    
    def __init__(self, x, y, largeur=250, hauteur=40):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.temperature = 20.0
        self.est_chaud = False
        
        # Couleurs
        self.couleur_normal = (0, 150, 255)    # Bleu
        self.couleur_chaud = (255, 165, 0)     # Orange
        self.couleur_fond = (50, 50, 50)
        self.couleur_texte = (255, 255, 255)
    
    def actualiser(self, temperature):
        """Met à jour la valeur et l'état"""
        if temperature is not None:
            self.temperature = temperature
            self.est_chaud = temperature > 25  # Seuil "Il fait chaud"
    
    def dessiner(self, surface):
        """Dessine l'indicateur sur la surface"""
        
        # 1. Fond de l'indicateur
        pygame.draw.rect(surface, self.couleur_fond,
                        (self.x, self.y, self.largeur, self.hauteur),
                        border_radius=8)
        
        # 2. Barre de température
        ratio = min(self.temperature / 40, 1.0)  # Échelle 0-40°C
        largeur_barre = int((self.largeur - 20) * ratio)
        
        # Couleur selon état
        couleur_barre = self.couleur_chaud if self.est_chaud else self.couleur_normal
        
        pygame.draw.rect(surface, couleur_barre,
                        (self.x + 10, self.y + 10, largeur_barre, self.hauteur - 20),
                        border_radius=5)
        
        # 3. Texte de la température
        police = pygame.font.Font(None, 24)
        texte_temp = police.render(f"{self.temperature}°C", True, self.couleur_texte)
        surface.blit(texte_temp, (self.x + self.largeur + 10, self.y + 5))
        
        # 4. Message "Il fait chaud" (si nécessaire)
        if self.est_chaud:
            self._dessiner_message_chaud(surface)
    
    def _dessiner_message_chaud(self, surface):
        """Dessine le message "Il fait chaud" avec animation"""
        # Animation de pulsation
        pulsation = abs(math.sin(pygame.time.get_ticks() * 0.005))
        intensite = int(100 + pulsation * 155)
        couleur_pulse = (255, intensite, 0)
        
        # Police pour le message
        police_grande = pygame.font.Font(None, 32)
        message = police_grande.render("Il fait chaud", True, couleur_pulse)
        
        # Position au-dessus de l'indicateur
        surface.blit(message, (self.x, self.y - 40))

class IndicateurLumiere:
    """
    Indicateur visuel de lumière
    Lumière élevée (>700) → brillant + message "Beaucoup de lumière"
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lumiere = 500
        self.est_brillant = False
        
        # Rayons du soleil autour du cercle
        self.rayons = []
        self._generer_rayons()
        
        # Couleurs
        self.couleur_normal = (255, 255, 150)  # Jaune clair
        self.couleur_brillant = (255, 255, 200) # Jaune brillant
        self.couleur_rayons = (255, 255, 100)
    
    def _generer_rayons(self):
        """Génère 12 rayons autour du cercle"""
        centre_x, centre_y = self.x + 30, self.y + 30
        
        for i in range(12):
            angle = (2 * math.pi * i) / 12
            longueur = 40
            fin_x = centre_x + math.cos(angle) * longueur
            fin_y = centre_y + math.sin(angle) * longueur
            self.rayons.append(((centre_x, centre_y), (fin_x, fin_y)))
    
    def actualiser(self, valeur_lumiere):
        """Met à jour la valeur et l'état"""
        if valeur_lumiere is not None:
            self.lumiere = valeur_lumiere
            self.est_brillant = valeur_lumiere > 700  # Seuil "Beaucoup de lumière"
    
    def dessiner(self, surface):
        """Dessine l'indicateur sur la surface"""
        centre_x, centre_y = self.x + 30, self.y + 30
        
        if self.est_brillant:
            # Mode brillant avec rayons
            self._dessiner_brillant(surface, centre_x, centre_y)
        else:
            # Mode normal
            self._dessiner_normal(surface, centre_x, centre_y)
        
        # Texte de la valeur
        police = pygame.font.Font(None, 24)
        texte_lum = police.render(f"Lumière: {self.lumiere}", True, (255, 255, 255))
        surface.blit(texte_lum, (self.x, self.y + 70))
    
    def _dessiner_normal(self, surface, centre_x, centre_y):
        """Dessine l'indicateur en mode normal"""
        # Cercle avec intensité proportionnelle à la lumière
        intensite = min(int(self.lumiere / 4), 255)
        couleur_cercle = (255, 255, intensite)
        pygame.draw.circle(surface, couleur_cercle, (centre_x, centre_y), 25)
    
    def _dessiner_brillant(self, surface, centre_x, centre_y):
        """Dessine l'indicateur en mode brillant avec animation"""
        # Animation de brillance
        pulsation = abs(math.sin(pygame.time.get_ticks() * 0.003))
        intensite = int(155 + pulsation * 100)
        couleur_brillante = (255, 255, intensite)
        
        # 1. Dessiner les rayons
        for rayon in self.rayons:
            # Rayons pulsants
            longueur_pulse = 40 * (0.8 + 0.4 * abs(math.sin(pygame.time.get_ticks() * 0.002)))
            start_x, start_y = rayon[0]
            end_x, end_y = rayon[1]
            
            # Direction normalisée
            dir_x = end_x - start_x
            dir_y = end_y - start_y
            length = math.sqrt(dir_x*dir_x + dir_y*dir_y)
            if length > 0:
                dir_x /= length
                dir_y /= length
            
            # Nouvelle position avec pulsation
            new_end_x = start_x + dir_x * longueur_pulse
            new_end_y = start_y + dir_y * longueur_pulse
            
            pygame.draw.line(surface, couleur_brillante, 
                           (start_x, start_y), (new_end_x, new_end_y), 4)
        
        # 2. Cercle brillant
        pygame.draw.circle(surface, couleur_brillante, (centre_x, centre_y), 30)
        
        # 3. Message "Beaucoup de lumière"
        self._dessiner_message_lumiere(surface)
    
    def _dessiner_message_lumiere(self, surface):
        """Dessine le message "Beaucoup de lumière" avec animation"""
        # Animation de pulsation
        pulsation = abs(math.sin(pygame.time.get_ticks() * 0.004))
        intensite = int(100 + pulsation * 155)
        couleur_pulse = (255, 255, intensite)
        
        # Police pour le message
        police_grande = pygame.font.Font(None, 32)
        message = police_grande.render("Beaucoup de lumière", True, couleur_pulse)
        
        # Position à droite de l'indicateur
        surface.blit(message, (self.x + 100, self.y))

class EffetSoleil:
    """
    Rayons de soleil dans le coin supérieur droit
    """
    
    def __init__(self):
        self.rayons = []
        self._generer_rayons()
    
    def _generer_rayons(self):
        """Génère 8 rayons orientés vers le coin supérieur droit"""
        soleil_x, soleil_y = 1800, 100  # Coin supérieur droit pour 1920x1080
        
        for i in range(8):
            # Angle orienté vers l'extérieur du coin
            angle = math.pi/4 * i + math.pi * 0.75
            
            longueur = random.randint(40, 80)
            fin_x = soleil_x + math.cos(angle) * longueur
            fin_y = soleil_y + math.sin(angle) * longueur
            
            self.rayons.append({
                'debut': (soleil_x, soleil_y),
                'fin': (fin_x, fin_y),
                'angle': angle,
                'longueur': longueur,
                'vitesse': random.uniform(0.5, 1.5)
            })
    
    def dessiner(self, surface, est_actif=True, intensite=1.0):
        """
        Dessine les rayons de soleil si actif
        intensite: 0.0 à 1.0 pour l'intensité des rayons
        """
        if not est_actif or intensite <= 0:
            return
        
        temps = pygame.time.get_ticks() * 0.001
        
        for rayon in self.rayons:
            # Animation pulsante
            pulsation = abs(math.sin(temps * rayon['vitesse']))
            longueur_pulse = rayon['longueur'] * (0.7 + 0.3 * pulsation)
            
            # Calcul de la position finale avec pulsation
            fin_x = rayon['debut'][0] + math.cos(rayon['angle']) * longueur_pulse
            fin_y = rayon['debut'][1] + math.sin(rayon['angle']) * longueur_pulse
            
            # Couleur avec transparence selon l'intensité
            alpha = int(100 + intensite * 155)
            couleur = (255, 255, 200, alpha)
            
            # Surface pour la transparence
            surf_transparente = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.line(surf_transparente, couleur, 
                           rayon['debut'], (fin_x, fin_y), 3)
            surface.blit(surf_transparente, (0, 0))
        
        # Dessiner le soleil (cercle central)
        soleil_x, soleil_y = 1800, 100
        
        # Soleil avec intensité variable
        rayon_soleil = int(30 + intensite * 20)
        couleur_soleil = (255, 255, int(100 + intensite * 155))
        
        pygame.draw.circle(surface, couleur_soleil, 
                         (soleil_x, soleil_y), rayon_soleil)
        pygame.draw.circle(surface, (255, 255, 200),
                         (soleil_x, soleil_y), int(rayon_soleil * 0.8))


class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920,1080))
        pygame.display.toggle_fullscreen()
        self.run = True
        self.sMatrix = [(120, 200), (1760, 360)]
        self.player = Player()
        self.animal = None
        self.animal_presence = False
        self.timerSpawnA = pygame.time.set_timer(eventSpawnA, 20000)
        self.timerMoveA = None
        self.background=pygame.image.load("resized_image.png")
        self.font = pygame.font.Font('Font/pokemon-ds-font.ttf', 72)
        self.text = None
        self.text_rect = None
        self.timerLight = pygame.time.set_timer(eventLight, 500)
        self.light = 600
        self.sky = pygame.Surface((1920, 1080))
        self.sky.set_alpha(128)
        self.indicateur_temp = IndicateurTemperature(x=50, y=50)
        self.indicateur_lumiere = IndicateurLumiere(x=50, y=150)
        self.effet_soleil = EffetSoleil()

    def start(self):
        while self.run:
            
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image,dest=self.player.body)
            if self.animal_presence:
                self.screen.blit(self.animal.sprite,dest=self.animal.body)
            if self.light < 350:
                self.screen.blit(self.sky, (0, 0))
            
            if self.animal_presence:
                if scream(self.player, self.animal) == 'appeuré':
                    self.animal = None
                    self.animal_presence = False
                    self.timerMoveA = None
                    self.timerSpawnA = pygame.time.set_timer(eventSpawnA, 20000)
                    self.text = None
                    self.text_rect = None
                temperature = 22.0  # REMPLACER PAR VOTRE LECTURE DE CAPTEUR
                            # 2. Mettre à jour les indicateurs
            self.indicateur_temp.actualiser(temperature)
            self.indicateur_lumiere.actualiser(self.light)
            
            # 3. Dessiner les rayons de soleil (si lumière suffisante)
            if self.light > 400:
                intensite = min(self.light / 1000, 1.0)
                self.effet_soleil.dessiner(self.screen, 
                                         est_actif=True,
                                         intensite=intensite)
            
            # 4. Dessiner les indicateurs (EN DERNIER pour qu'ils soient visibles)
            self.indicateur_temp.dessiner(self.screen)
            self.indicateur_lumiere.dessiner(self.screen)
            
            if self.animal_presence:
                if scream(self.player, self.animal) == 'appeuré':
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or grove_quit.player_quit:
                    self.run = False
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
                if event.type == eventLight:
                    self.light = lightSensor()
                        
            if self.text is not None:
                self.screen.blit(self.text, self.text_rect)
                    
            movement(self.player, gmap)
                
            pygame.display.update()
