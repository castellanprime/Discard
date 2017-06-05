
from enum import Enum

class ShapeColour(Enum):
	RED = 1
	BLUE = 2
	GREEN = 3
	YELLOW = 4

class CardColour(Enum):
	BLACK = 1
	WHITE = 2

class Shapes(Enum):
	CROSS = 1
	SQUARE = 2
	TRIANGLE = 3
	CIRCLE = 4
	CUP = 5

class PlayerState(Enum):
	PLAYING = 1					# Currently playing
	PLAYED = 2					# Just played before currently playing
	PAUSED = 3					# Waiting to play

class GameState(Enum):
	WIN = 1						# Player won 
	LOSE = 2					# Player lost
	INVALIDMOVE = 3
	NOACTION = 4
	DRAW = 5 					# If the game is timed

class CardType(Enum):
	SPECIAL=1
	NORMAL=2


