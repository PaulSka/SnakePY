#!/usr/bin/python
# -*- coding: utf-8 -*-

#**************************************************
# SnakePY (Coding party projet)
#**************************************************

#Importation des modules
import curses
import core
from optparse import OptionParser
import sys

#GLOBAL
global config, game

def initCurse():
    #On initialise notre fenêtre
    curses.initscr()
    #Couleur active !
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.curs_set(0)


def closeCurse():
    #On détruit les fenêtres curses
    curses.endwin()
    #On sort du script
    exit()

def loadLogo():
    #On charge le fichier logo
    f = open('ASCII.art', 'rb')
    #On recupere les lignes
    lines = f.readlines()    
    #On ferme le fichier
    f.close()
    return lines

def createNewWin(curses):
    """
    On créer une nouvelle fenetre Curse
    """

    #On dimensionne notre fenetre
    x = config.rawConfig.getint("GLOBAL", "x")
    y = config.rawConfig.getint("GLOBAL", "y")

    #On créer la fenêtre
    win = curses.newwin(x,y,0,0)

    #On affecte les différents paramètres a notre fenêtre
    win.keypad(1)
    win.nodelay(1)
    win.border(0)

    return win

def destroyWin():
    """
    Fonction permettant de détruire les
    fenêtres curses
    """
    curses.endwin()

def menu():

    #On créer une nouvelle fenetre
    win = createNewWin(curses)

    #On charge le logo et on l'affiche
    logoLines = loadLogo()
    i = 1
    for line in logoLines:
        win.addstr(i, 16, line, curses.color_pair(2))
        i+=1
    win.border(0)

    chooseMenu = 0    
    #On ajoute les entrées
    win.addstr(1, 4, 'SnakePY', curses.color_pair(1))
    win.addstr(2, 4, 'Choose option', curses.color_pair(1))
    win.addstr(3, 4, '1. Launch game', curses.color_pair(1))
    win.addstr(4, 4, '2. Show HighScore', curses.color_pair(1))
    win.addstr(5, 4, '3. Credits', curses.color_pair(1))
    win.addstr(6, 4, '4. Exit game', curses.color_pair(1))
    win.addstr(7, 4, '')

    while chooseMenu != ord('4'):
        #On récupere la touche appuyée par l'utilisateur
        chooseMenu = win.getch()
        #Si il s'agit du 1 ...
        if chooseMenu == ord('1'):
            #...on lance le jeu
            destroyWin()
            launchGame()
        #Si il s'agit du 2 ...
        elif chooseMenu == ord('2'):
            #...on affiche le highscore
            destroyWin()
            showHG()
        #Si il s'agit du 3 ...
        elif chooseMenu == ord('3'):
            #... on affiche les crédits
            destroyWin()
            showCredits()
    #Si on sort de la boucle (4), alors on
    #détruit les fenetres
    destroyWin()

    #On ferme toutes les fenêtres de curses
    closeCurse()
    
def launchGame():
    """
    Génére une nouvelle fenêtre curse et lance le jeu
    """    
    # On rejoint la partie
    game.join()

    #On affecte le nom
    game.player.setName(options.name)

    #On créer une nouvelle fenetre
    win = createNewWin(curses)

    #On creer notre premiere pomme...
    win.addch(game.apple.coordx, game.apple.coordy, 'O', curses.color_pair(3))

    #On indique la direction par defaut du serpent, il ira par defaut a droite
    key = curses.KEY_RIGHT

    #On effectue une boucle infinie tant que la touche Echap (27) n'est pas
    #pressée.
    while key != 27:
        #On ajoutte le score a la ligne 0, colonne 2
        #Le score est calcule en recuperant la longueur du serpent actuel
        #et en retirant 2 (sa valeur initiale)	
        win.addstr(0,2,' Joueur : %s Score : %s ' %(game.player.name, str(game.player.score)), curses.color_pair(1))

        #On calcul un mouvement de ralentissement dependant de la longueur du
        #serpent
        win.timeout(180+ ( (len(game.snake.oSnake)-2) % 10- (len(game.snake.oSnake)-2) ) * 3 )

        #On 'hook' les touches
        getkey = win.getch()

        #On recupere la valeur de la touche par defaut
        key = key if getkey==-1 else getkey

        #Suivant la touche pressée, on modifie les positions de notre serpent
        game.snake.move(key)

        #On supprime les derniers elements sur lequel le Snake passe
        win.addch(game.snake.oSnake[len(game.snake.oSnake)-1][1],
            game.snake.oSnake[len(game.snake.oSnake)-1][0],' ')

        #On supprime un element du snake pour eviter la collision
        if win.inch(game.snake.oSnake[0][1], game.snake.oSnake[0][0]) & 255 == 32:
            game.snake.oSnake.pop()

        #Si on passe sur un element O	
        elif win.inch(game.snake.oSnake[0][1],game.snake.oSnake[0][0]) & 255 == ord('O'):
            #On ajoutte 1 point a notre Joueur
            game.player.addPoint()

            #On recalcule des nouvelles coordonnees pour la pomme
            game.apple.newApple()
            #On verifie les nouvelles coordonnees
            while game.apple.checkApple(game.snake.oSnake) != True:
                game.apple.newApple()

            #On l'affiche a l'ecran
            win.addch(game.apple.coordx, game.apple.coordy, 'O', curses.color_pair(3))
		
        else:
            break

        #On affiche une partie de notre Snake
        win.addch(game.snake.oSnake[0][1],game.snake.oSnake[0][0],'X', curses.color_pair(2))


    #Si on sort de la boucle (GameOver), alors on
    #détruit les fenetres
    destroyWin()

    #A la fin de la partie (game over), on affiche l'écran    
    showGameOver()

def showGameOver():
    """
    Affiche l'écran GameOver
    """

    #On créer une nouvelle fenetre
    win = createNewWin(curses)

    win.addstr(1, 4, 'GAME OVER', curses.color_pair(3))
    win.addstr(2, 4, 'Your Score', curses.color_pair(1))    
    win.addstr(3, 4, '%s - %s' %(game.player.name, game.player.score), curses.color_pair(1))
    win.addstr(4, 4, 'Press 1 to return previous menu', curses.color_pair(1))
    win.addstr(5, 4, '')

    #Ajout dans le highscore
    game.highscore.addHighScore(game.player.name, game.player.score)
    game.highscore.writeHighScore()

    key = 0
    #Tant que la touche 1 n'est pas pressée...
    #while key!= 343 or key!=10:
    while key != ord('1'):
        #On attend et on 'hook' les touches
        key = win.getch()

    #Si on sort de la boucle (1), alors on
    #détruit les fenetres
    destroyWin()

    #A la fin de la partie (game over), on affiche l'écran    
    menu()

def showHG():
    """
    Affiche l'écran de highscore
    """

    #On créer une nouvelle fenetre
    win = createNewWin(curses)
    
    win.addstr(1, 4, 'SnakePY HighScore', curses.color_pair(1))
    win.addstr(2, 4, 'Press 1 to return previous menu', curses.color_pair(1))
    win.addstr(3, 4, '')


    #On boucle sur les HighScore
    i = 4
    #Pour chaque entrée dans le highscore...
    for hg in game.highscore.showHighScore():
        #On ajoutte une ligne
        win.addstr(i, 4, "%s -- %s" %(hg[0], hg[1]), curses.color_pair(1))
        i+=1

    chooseMenu = 0
    #Tant que la touche 1 n'est pas pressée...
    while chooseMenu!= ord('1'):
        #On attend et on 'hook' les touches
        chooseMenu = win.getch()

    #Si on sort de la boucle (4), alors on
    #détruit les fenetres
    destroyWin()

    #...sinon on sort de la boucle et on affiche de
    #de nouveau le menu    
    menu()

def showCredits():
    """
    Affiche les crédits via le fichier CREDITS
    """

    #On créer une nouvelle fenetre
    win = createNewWin(curses)

    win.addstr(1, 4, 'CREDITS', curses.color_pair(1))
    win.addstr(2, 4, 'Press 1 to return previous menu', curses.color_pair(1))
    win.addstr(3, 4, '')

    #On charge le fichier credits
    f = open('CREDITS', 'rb')
    #On recupere les lignes
    lines = f.readlines()    
    #Pour chaque ligne présentes....
    i = 4
    for line in lines:
        #...on ajoutte les infos en supprimant les 'blancs' (strip())
        win.addstr(i, 4, line.strip(), curses.color_pair(1))
        i+=1
    chooseMenu = 0
    #Tant que la touche 1 n'est pas pressée...
    while chooseMenu!= ord('1'):
        #On attend et on 'hook' les touches
        chooseMenu = win.getch()

    #Si on sort de la boucle (1), alors on
    #détruit les fenetres
    destroyWin()

    #...sinon on sort de la boucle et on affiche de
    #de nouveau le menu    
    menu()

#-------------------------
#Initialisation du jeu 
#-------------------------

#Partie OptParse
parser = OptionParser()
parser.add_option('-n', '--name', dest="name", help="Name", default="Snake", type="string")
(options, args) = parser.parse_args()

#On instancie notre classe Config
config = core.Config()

try:
    #On initialise Curses()
    initCurse()

    #On dimensionne notre fenetre
    x = config.rawConfig.getint("GLOBAL", "x")
    y = config.rawConfig.getint("GLOBAL", "y")

    #On instancie notre partie
    game = core.Game(config)

    #On affiche le menu
    menu()

except:
    #On ferme curse
    closeCurse()
    sys.exit("Error")

