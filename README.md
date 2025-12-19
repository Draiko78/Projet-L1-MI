# Projet-L1-MI

	Projet L1 MI, jeu interactif "L'Horticulteur"


## Assets

	- https://penzilla.itch.io/farming-and-garden-icon-pack
	- https://imayazing.itch.io/garden-graphics
	- https://jinhzaki.itch.io/free-gardening-tools-assets-32x32
	- https://pokemon-floral-tempus.fandom.com/wiki/Alolan_Raticate
	- https://pokemon-floral-tempus.fandom.com/wiki/Alolan_Rattata
	- https://pokemon-floral-tempus.fandom.com/wiki/Rattata
	- https://pokemon-floral-tempus.fandom.com/wiki/Raticate
	- https://fontstruct.com/fontstructions/show/1182741/pokemon-ds-font


### requirments

	- pygame
	- flask
	- RPi.GPIO
	- grove


#### Branchement des capteurs

	- Le joystick sur le pin A0
	- Le capteur de son sur le pin A6
	- Le capteur de luminosité sur le pin A4
	- le bouton sur le pin D18


##### Lancer le Projet

	Pour lancer le projet, veuillez installer les modules nécessaires s'ils ne le sont pas déjà 
	puis dans un terminal utilisez la commande suivante (depuis le repertoire  du Projet):

	python3 app.py

	Puis ouvrez votre navigateur et entrez l'adresse (testé sur firefox):
	http://localhost:5000


###### Gameplay

	Déplacez vous avec le joystick
	Avec le bouton :
		- Appuyez une fois pour creuser
		- Deux fois pour planter une graine
		- Trois fois pour la faire pousser (ne marche que si c'est le jour)
	Lorsque un animal essaye de vous manger vos salades approchez vous de lui et criez lui dessus avec le capteur de son pour le faire fuir
	De base le jeu se déroule de jour, mais si la luminosité détecté par le capteur de luminosté ets trop basse, le jeu passera en mode nuit.
	Pour revenir au jour, illuminez le capteur de luminosité. 
	
