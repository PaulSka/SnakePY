#!/usr/bin/python


"""
Partie GUI pour le snake
"""

##TODO
#Voir fichier TODO

import curses
import core

def clearScreen():
    """
    Efface l'ecran et redessine les bordures
    """
    win.clear()
    #On dessine les contours
    win.border(0)


def launchGame():

    clearScreen()

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

    clearScreen()

def showHG():
    clearScreen()    
    win.addstr(4, 4, 'SnakePY HighScore')
    win.addstr(5, 4, 'Press 1 to return previous menu')
    #On boucle sur les HighScore
    x = 7
    for hg in game.highscore.showHighScore():
        win.addstr(x, 4, "%s -- %s" %(hg[0], hg[1]))
        x+=1
    stop = 0
    while stop!= ord('1'):
        stop = win.getch()
    menu()
    return

def showCredits():
    import time
    clearScreen()    
    win.addstr(4, 4, 'SnakePY Credits')
    win.addstr(5, 4, 'Press 1 to return previous menu')
    x = 7
    #On charge le fichier credits
    f = open('CREDITS', 'rb')
    #On recupere la ligne
    lines = f.readlines()    
    #On affiche les lignes
    for line in lines:
        win.addstr(x, 4, line.strip())
        x+=1
    stop = 0
    while stop!= ord('1'):
        stop = win.getch()
    menu()
    return
    
    
def menu():
    #Menu
    x = 0

    clearScreen()

    #On boucle pour le menu    
    while x!= ord('4'):
        #On ajoute les entrees
        win.addstr(4, 4, 'SnakePY')
        win.addstr(5, 4, 'Choose option')
        win.addstr(6, 4, '1. Launch game')
        win.addstr(7, 4, '2. Show HighScore')
        win.addstr(8, 4, '3. Credits')
        win.addstr(9, 4, '4. Exit game')
        #On recupere la touche appuye par l'utilisateur
        x = win.getch()
        if x == ord('1'):
            #Si il s'agit du 1 ...
            launchGame()
        if x == ord('2'):
            showHG()
        if x == ord('3'):
            showCredits()
    return    

#On initialise notre fenetre
curses.initscr()
curses.curs_set(0)

#On instancie notre classe Config
config = core.Config()

#On dimensionne notre fenetre
x = config.rawConfig.getint("GLOBAL", "x")
y = config.rawConfig.getint("GLOBAL", "y")
win = curses.newwin(x,y,0,0)

#?
win.keypad(1)
win.nodelay(1)

#On instancie notre partie
game = core.Game(config)

      
#On affiche le menu
menu()

curses.endwin()
exit()
