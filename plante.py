import pygame


def plantation(gmap,playerChar,map_base):

    soleil=True
    my = playerChar.body.left//40
    mx = playerChar.body.top//40
    pos_x=(my+1)*40
    pos_y=(mx+1)*40
    car_voulu=pygame.Rect(pos_x,pos_y,40,40)


    image_plt=pygame.image.load("trou_sol.png")
    image_plt=pygame.transform.scale(image_plt,(40,40))

    image_grn=pygame.image.load("plante_debut.png")
    image_grn=pygame.transform.scale(image_grn,(40,40))
    
    image_sld=pygame.image.load("salade.png")
    image_sld=pygame.transform.scale(image_sld,(40,40))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN :
            if event.key==pygame.K_k:
                if  gmap[mx][my+1] == 0 and gmap[mx-1][my+1]==2 :
                    #permet de creuser le trou
                    plt = pygame.Rect((gmap[mx-1][my+1], gmap[mx-1][my+1]),(40,40))
                    screen.blit(image_plt,dest=plt)
                    gmap[mx-1][my+1]=3

                elif gmap[mx][my+1] == 0 and gmap[mx-1][my+1]==3 :
                    #permet de planter la graine
                    grn = pygame.Rect((gmap[mx-1][my+1], gmap[mx-1][my+1]),(40,40))
                    screen.blit(image_grn,dest=grn)
                    gmap[mx-1][my+1]=4
                
                elif gmap[mx][my+1] == 0 and gmap[mx-1][my+1]==4 :
                #permet de déterrer la plante/graine
                    screen.blit(map_base,dest=car_voulu,area=car_voulu)
                    gmap[mx-1][my+1]=2
            
            if event.key==pygame.K_j and gmap[mx][my+1] == 0 and gmap[mx-1][my+1]==4 and soleil:
                #permet d'arroser la plante (la fait pousser que s'il y a du soleil)
                sld=pygame.Rect((gmap[mx-1][my+1],gmap[mx-1][my+1]),(40,40))
                screen.blit(image_sld,dest=sld)

                sld=pygame.Rect((gmap[mx-1][my+1],gmap[mx-1][my+1]),(40,40))
                screen.blit(image_sld,dest=sld)
