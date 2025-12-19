import pygame
from random import randint

class Animal:
	def __init__(self, saladMatrix):
		self.proximities = [200, 160, 120, 80]
		self.model = randint(0, 3)
		self.proxFear = self.proximities[self.model]
		self.sprite = pygame.image.load(f"game/assets/rat0{self.model+1}.png")
		self.sprite = pygame.transform.scale(self.sprite, (40, 40))
		self.body = pygame.Rect((920, 1000),(40,40))
		self.speed = randint(400, 600)
		self.sMatrix = saladMatrix
		self.target = saladMatrix[randint(1, len(saladMatrix))-1]
	
	def moveToSalad(self, gmap, font):
		"""Déplacement et logique de nourriture du rat"""
		direction = randint(0, 1)
		my_A = self.body.left//40
		mx_A = self.body.top//40
		
		if direction == 0:
			if self.target[0] > self.body.left and gmap[mx_A][my_A+1] != 1:
				self.body.left += 40
			elif self.target[0] < self.body.left and gmap[mx_A][my_A-1] != 1:
				self.body.left -= 40
			else:
				if self.target[1] < self.body.top and gmap[mx_A-1][my_A] != 1:
					self.body.top -= 40 
				elif self.target[1] > self.body.top and gmap[mx_A+1][my_A] != 1:
					self.body.top += 40
		elif direction == 1:
			if self.target[1] < self.body.top and gmap[mx_A-1][my_A] != 1:
					self.body.top -= 40 
			elif self.target[1] > self.body.top and gmap[mx_A+1][my_A] != 1:
					self.body.top += 40
			else:
				if self.target[0] > self.body.left and gmap[mx_A][my_A+1] != 1:
					self.body.left += 40
				elif self.target[0] < self.body.left and gmap[mx_A][my_A-1] != 1:
					self.body.left -= 40
		
		salad_rect = pygame.Rect(self.target[0], self.target[1], 40, 40)
			
		if self.body.colliderect(salad_rect):
			self.sMatrix.remove(self.target)
			if len(self.sMatrix) != 0:
				self.target = self.sMatrix[randint(1, len(self.sMatrix))-1]
				text = font.render("Attention l'animal a mangé la salade !!", False, (255, 0, 0))
				gmap[self.target[1]//40][self.target[0]//40] = 2
				return text, True
			else:
				text = font.render("Vous avez perdu...", False, (255, 0, 0))
				return text, False
			
		text = font.render("Un animal essaye de manger vos salades !!!", False, (255, 0, 0))
		return text, True
