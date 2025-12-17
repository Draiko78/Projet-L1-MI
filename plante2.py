import pygame

def plantation(gmap, playerChar, event):
    soleil = True

    # On cible la case juste au-dessus du joueur
    my = playerChar.body.left // 40
    mx = (playerChar.body.top // 40) - 1

    # On vérifie que l'événement passé par Screen est un appui de touche
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_k:
            # Si c'est de l'herbe (2), on fait un trou (3)
            if gmap[mx][my+1] == 2:
                gmap[mx][my+1] = 3
            # Si c'est un trou (3), on plante (4)
            elif gmap[mx][my+1] == 3:
                gmap[mx][my+1] = 4
            # Si c'est une graine (4), on fait pousser la salade (5)
            elif gmap[mx][my+1] == 4 and soleil:
                gmap[mx][my+1] = 5
                return True, ((my+1)*40, mx*40)
    return False, ()
