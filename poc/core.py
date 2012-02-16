"""
Partie Core
"""

##TODO
#Voir fichier TODO

import random
import cPickle
import os
import operator
import ConfigParser

class Player():
	"""
	Creation de la classe Player
	"""

	score = 0

	def __init__(self, name="Snake"):
		"""
		Methode execute a l'instanciation de la classe Player
		On fixe le nom du joueur a Snake par defaut
		"""
		self.setName(name)

	def setName(self, name):
		"""
		Methode permettant de fixer le nom du joueur
		"""
		self.name = name

	def addPoint(self):
		"""
		Methode permettant d'ajouter 1 point au score du joueur
		"""
		self.score +=1

class HighScore():
	"""
	Creation de la classe HighScore
	"""
	def __init__(self):
		"""
		Methode execute a l'instanciation de la classe HighScore
		"""
		#On charge notre fichier pickle si il existe,
		#sinon on le creer
		self.oFullPath = 'highscore.pkl'
		if os.path.isfile(self.oFullPath):
			self.highScore = cPickle.load(open(self.oFullPath, 'rb'))
		else:
			self.highScore = {}

	def addHighScore(self, player, score):
		"""
		methode permettant d'ajouter un resultat au HighScore
		"""
		self.highScore[player] = score

	def writeHighScore(self):
		"""
		Methode permettant de sauvegarder les HighScores
		Structure du HighScore
		{
			'John': 16,
			'Bryan': 1,
			'Joe': 9,
			...
			'Snake': 8,
		}
		"""
		if isinstance(self.highScore, list):
			self.highScore = dict(self.highScore)
		cPickle.dump(self.highScore, open(self.oFullPath, 'wb'))
		
	def showHighScore(self):
		"""
		Methode permettant d'afficher les meilleurs HighScores
		"""
		#On doit tester si la liste de scores est vide (initialisation)
		#ou contient deja des valeurs
		#
		
		return sorted(self.highScore.iteritems(), key=operator.itemgetter(1), reverse=True)

class Snake():
	"""
	Creation de la classe Snake
	"""

	def __init__(self, initPos, lSnake=2):
		"""
		Methode execute a l'instanciation de la classe Snake
		"""
		self.oSnake = self.createSnake(initPos, lSnake)
	
	def createSnake(self, initPos, lSnake):
		"""
		Methode permettant de creer le Snake
		initPos est un couple x,y
		lSnake represente la longueur par defaut (2) 
		"""

		#On creer notre Snake sous la forme de coordonnees
		#[x,y]
		snake = []
		#Pour la longueur souhaite, on fait 'grandir'' notre
		#Snake
		for i in range(lSnake):
			snake.append([initPos[0], initPos[1]+i])
		
		#On renvoie les coordonnes du Snake
		return snake

	def move(self, key):
		"""
		Methode pour le mouvement du snake
		"""
		if key == 260:
			self.oSnake.insert(0, [self.oSnake[0][0] -1, self.oSnake[0][1]])
		elif key == 261:
			self.oSnake.insert(0, [self.oSnake[0][0] +1, self.oSnake[0][1]])
		elif key == 259:
			self.oSnake.insert(0, [self.oSnake[0][0], self.oSnake[0][1] -1])
		elif key == 258:
			self.oSnake.insert(0, [self.oSnake[0][0], self.oSnake[0][1] +1])

class Apple():
	"""
	Classe concernant la pomme
	"""

	def __init__(self, maxX, maxY):
		self.maxX = maxX
		self.maxY = maxY
		self.newApple()

	def newApple(self):
		"""
		Methode permettant de creer les coordonnes d'une pomme
		La pomme ne doit pas etre creer aux coordonnes du Snake
		"""
		self.coordx = random.randrange(1, self.maxX-1)
		self.coordy = random.randrange(1, self.maxY-1)

	def checkApple(self, snakePos):
		"""
		Methode verifiant si les nouvelles coordonnees de la pomme
		ne sont pas sur les coordonnees du Snake
		"""
		if [self.coordx, self.coordy] in snakePos:
			return False
		elif [self.coordx, self.coordy] not in snakePos:
			return True

class Config():
	"""
	Classe concernant la configuration
	"""

	def __init__(self):
		self.rawConfig = ConfigParser.ConfigParser()
		self.rawConfig.read('conf.ini')
