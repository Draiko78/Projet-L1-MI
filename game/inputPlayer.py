import pygame
from capteurs import joystick, sound_sensorv2, grove_button

def movement(playerChar, gmap):
	"""Déplacement du joueur"""
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
	"""Cri du joueur"""
	sound_level = sound_sensorv2.soundSensor()
	dToTarget = (abs(player.body.centerx - target.body.centerx), abs(player.body.centery - target.body.centery))
	if dToTarget[0] <= target.proxFear and dToTarget[1] <= target.proxFear:  
		if sound_level > 750:
			return 'appeuré'
	return "L'animal n'a pas l'air appeuré"

def plantation(gmap, playerChar, soleil):
    """Fonction pour planter"""
    pressed = grove_button.is_button_pressed()
    if pressed:
        # Get player's current position
        player_col = playerChar.body.left // 40 
        player_row = playerChar.body.top // 40
        
        # Check tile above the player
        tile_row = player_row - 1
        tile_col = player_col + 1
        
        # Ensure we're within bounds
        if 0 <= tile_row < len(gmap) and 0 <= tile_col < len(gmap[0]):
            # If it's plantable grass (2), make a hole (3)
            if gmap[tile_row][tile_col] == 2:
                gmap[tile_row][tile_col] = 3
                plant_state = 3
            # If it's a hole (3), plant seeds (4)
            elif gmap[tile_row][tile_col] == 3:
                gmap[tile_row][tile_col] = 4
                plant_state = 4
            # If it's seeds (4) and sunny, grow salad (5)
            elif gmap[tile_row][tile_col] == 4 and soleil:
                gmap[tile_row][tile_col] = 5
                return True, (tile_col * 40, tile_row * 40), 5
    
    plant_state = None
    return False, (), plant_state
