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

#On instancie notre partie
game = core.Game(config)

# On rejoint la partie
game.join()

#On creer notre premiere pomme...
win.addch(game.apple.coordx, game.apple.coordy, 'O')

#On indique la direction par defaut du serpent, il ira par defaut a droite
key = curses.KEY_RIGHT

#On effectue une boucle infinie tant que la touche Echap (27) n'est pas
#presse
while key != 27:
	#On ajoutte le score a la ligne 0, colonne 2
	#Le score est calcule en recuperant la longueur du serpent actuel
	#et en retirant 2 (sa valeur initiale)	
	win.addstr(0,2,' Joueur : %s Score : %s ' %(game.player.name, str(game.player.score)))

	#On calcul un mouvement de ralentissement dependant de la longueur du
	#serpent
	win.timeout(180+ ( (len(game.snake.oSnake)-2) % 10- (len(game.snake.oSnake)-2) ) * 3 )

	#On 'hook' les touches
	getkey = win.getch()

	#On recupere la valeur de la touche par defaut
	key = key if getkey==-1 else getkey

	#Suivant la touche presse, on modifie les positions de notre serpent
	game.snake.move(key)

	#On supprime les derniers elements sur lequel le Snake passe
	win.addch(game.snake.oSnake[len(game.snake.oSnake)-1][1],
	    game.snake.oSnake[len(game.snake.oSnake)-1][0],' ')

	#On supprime un element du snake pour eviter la collision
	if win.inch(game.snake.oSnake[0][1],
	        game.snake.oSnake[0][0]) & 255 == 32:
  		game.snake.oSnake.pop()

	#Si on passe sur un element O	
	elif win.inch(game.snake.oSnake[0][1],
	      game.snake.oSnake[0][0]) & 255 == ord('O'):
		#On ajoutte 1 point a notre Joueur
		game.player.addPoint()
	
		#On recalcule des nouvelles coordonnees pour la pomme
		game.apple.newApple()
		#On verifie les nouvelles coordonnees
		while game.apple.checkApple(game.snake.oSnake) != True:
			game.apple.newApple()

		#On l'affiche a l'ecran
		win.addch(game.apple.coordx, game.apple.coordy, 'O')
		
	else:
	  break

	#On affiche une partie de notre Snake
	win.addch(game.snake.oSnake[0][1],game.snake.oSnake[0][0],'X')

#On met a jour le HighScore et on sauvegarde.
game.highscore.addHighScore(game.player.name, game.player.score)
game.highscore.writeHighScore()

curses.endwin()
