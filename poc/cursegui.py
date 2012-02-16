#!/usr/bin/python


"""
Partie GUI pour le snake
"""

##TODO
#Voir fichier TODO

import curses
import core


#On initialise notre fenetre
curses.initscr()
curses.curs_set(0)

#On instancie notre classe Config
config = core.Config()

#On dimensionne notre fenetre
x = config.rawConfig.getint("GLOBAL", "x")
y = config.rawConfig.getint("GLOBAL", "y")
win = curses.newwin(x,y,0,0)

#On dessine les contours
win.border(0)

#?
win.keypad(1)
win.nodelay(1)

#On instancie notre Snake en lui indiquant sa position par defaut
#et sa taille par defaut
snake = core.Snake([30,7], 2)

#On instancie notre Joueur
player = core.Player()
player.setName(config.rawConfig.get("PLAYER", "name"))

#On instancie notre classe Apple
apple = core.Apple(x, y)

#On instancie notre classe HighScore
highscore = core.HighScore()

#On creer notre premiere pomme...
win.addch(apple.coordx, apple.coordy, 'O')

#On indique la direction par defaut du serpent, il ira par defaut a droite
key = curses.KEY_RIGHT

#On effectue une boucle infinie tant que la touche Echap (27) n'est pas
#presse
while key != 27:
	#On ajoutte le score a la ligne 0, colonne 2
	#Le score est calcule en recuperant la longueur du serpent actuel
	#et en retirant 2 (sa valeur initiale)	
	win.addstr(0,2,' Joueur : %s Score : %s ' %(player.name, str(player.score)))

	#On calcul un mouvement de ralentissement dependant de la longueur du
	#serpent
	win.timeout(180+ ( (len(snake.oSnake)-2) % 10- (len(snake.oSnake)-2) ) * 3 )

	#On 'hook' les touches
	getkey = win.getch()

	#On recupere la valeur de la touche par defaut
	key = key if getkey==-1 else getkey

	#Suivant la touche presse, on modifie les positions de notre serpent
	snake.move(key)

	#On supprime les derniers elements sur lequel le Snake passe
	win.addch(snake.oSnake[len(snake.oSnake)-1][1],snake.oSnake[len(snake.oSnake)-1][0],' ')

	#On supprime un element du snake pour eviter la collision
	if win.inch(snake.oSnake[0][1],snake.oSnake[0][0]) & 255 == 32:
		snake.oSnake.pop()

	#Si on passe sur un element O	
	elif win.inch(snake.oSnake[0][1],snake.oSnake[0][0]) & 255 == ord('O'):
		#On ajoutte 1 point a notre Joueur
		player.addPoint()
	
		#On recalcule des nouvelles coordonnees pour la pomme
		apple.newApple()
		#On verifie les nouvelles coordonnees
		while apple.checkApple(snake.oSnake) != True:
			apple.newApple()

		#On l'affiche a l'ecran
		win.addch(apple.coordx, apple.coordy, 'O')
		
	else: break

	#On affiche une partie de notre Snake
	win.addch(snake.oSnake[0][1],snake.oSnake[0][0],'X')

#On met a jour le HighScore et on sauvegarde.
highscore.addHighScore(player.name, player.score)
highscore.writeHighScore()

curses.endwin()
