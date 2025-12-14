import pygame
from capteurs import joystick, sound_sensorv2

def movement(playerChar, gmap):
	directions = joystick.jsDirection()
	if directions != []:
		my = playerChar.body.left//40
		mx = playerChar.body.top//40

		if 'right' in directions and gmap[mx][my+1] == 0:
			playerChar.body.left+=40
			playerChar.image=playerChar.image_droite
			my = playerChar.body.left//40
		if 'left' in directions and gmap[mx][my-1] == 0: 
			playerChar.body.left-=40
			playerChar.image=playerChar.image_gauche
			my = playerChar.body.left//40
		if 'up' in directions and gmap[mx-1][my] == 0:
			playerChar.body.top-=40
			playerChar.image=playerChar.image_dos
			mx = playerChar.body.top//40
		if 'down' in directions and gmap[mx+1][my] == 0:
			playerChar.body.top+=40
			playerChar.image=playerChar.image_face
			mx = playerChar.body.top//40

def scream(player, target):
	sound_level = sound_sensorv2.soundSensor()
	dToTarget = (abs(player.body.centerx - target.body.centerx), abs(player.body.centery - target.body.centery))
	if dToTarget[0] <= target.proxFear and dToTarget[1] <= target.proxFear:  
		if sound_level > 750:
			return 'appeuré'
	return "L'animal n'a pas l'air appeuré"
