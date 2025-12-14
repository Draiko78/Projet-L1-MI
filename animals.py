import pygame
from random import randint

class Animal:
	def __init__(self, saladMatrix):
		self.proximities = [200, 160, 120, 80]
		self.model = randint(0, 3)
		self.proxFear = self.proximities[3]
		self.sprite = pygame.image.load(f"assets/rat0{3+1}.png")
		self.body = pygame.Rect((920, 1000),(40,40))
		self.speed = randint(500, 1500)
		self.target = saladMatrix[randint(1, len(saladMatrix))-1]
	
	def moveToSalad(self, gmap):
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
