"""
	This module contains the game logic
	for Discard

"""
from collections import nametuple
from random import shuffle
from cards import SpecialCard, NormalCard
from enums import ShapeColour, CardColour, Shapes, GameState, PlayerState, CardType
from player import Player

"""
	Rules:
	'1' - 	Pick a card
	'2' - 	Pick two cards
	'?' - 	Ask for any Normal Card. If the player desires, the card can be
			accompanied by these cards with their effects
			-	'->': Skip everybody and play again
			-	'1': Everybody picks one card and you play again
			-	'2': Everybody picks two cards and you play again
	'-'	-	Discard any Normal Cards you have with it. If the player desires, 
			the card can be	accompanied by these cards with their effects
			-	'1': The player discards one extra card.
			- 	'2': The player discards two extra cards.
			- 	'?': Remove a SpecialCard from the first player that has a Special Card.
				If there are no	special cards, the player can discard one extra card.
			-	'->': Remove a SpecialCard from the next player in turn. If the player
				does not have a SpecialCard, the player can discard one extra card.

	Algorithm:
		- Check to see what type of card has been played.
			- If the card is a NormalCard, check if the shape/colour matches the 
			the card at the top of the deck
			- If the card is a SpecialCard, check if the char/colour matches the 
			the card at the top of the deck.
		- If the card doesnt match, punish the player who has played that card with two cards
		and then mark him/her as PlayerState.PLAYED
		- If the card matches, 
			- If the card is a Special Card, execute the actions:
				- If the card is a '1' or a '2' or a '->', then execute the action only if
				the player has not played either a '?' or '-'.
				- If the card is a '?' or a '-', then ask if you want to stack another
				Special Card and execute the action.   
			- If the card is a normal Card, continue and go to the next player.

	Playing the game should be as follows:

	- Initialise players.
	- Initialise game.
	- Start Game with chosen current player
		While no player has won:
		- The current player looks at his/her cards and makes a decision
			(player.checkCards())
		- The current player then picks those cards and hands them over to the game.
			(player.play())
		- The game checks the cards according to the algorithm described earlier and then 
			makes a decision. 

"""


class DiscardGame(object):

	game_deck = []
	played_deck = []
	game_state = {}
	players = []

	def __init__(self, players):
		for player in players:
			player.join(self)
		self.players = players
		for player in self.players:
			self.game_state[player] = PlayerState.PAUSED
		self.setupDecks()


	def setupDecks(self):
		self.colours = [ShapeColour.RED, ShapeColour.BLUE, ShapeColour.GREEN, ShapeColour.YELLOW]
		self.shapes = [Shapes.CROSS, Shapes.SQUARE, Shapes.TRIANGLE, Shape.CIRCLE, Shape.CUP]
		self.initDeck()
		self.deal()

	def initDeck(self):
		normal_deck = self._initNormalCardDeck()
		special_deck = [card for deck in self._initSpecialCardDeck() \
						for card in deck]
		self.game_deck.append(normal_deck)
		self.game_deck.append(special_deck)
		self.game_deck = [card for deck in self.game_deck for card in deck] 
		shuffle(self.game_deck)

	def deal(self):
		num_of_players = len(self.players)
		if num_of_players == 2:
			num_cards_to_deal = 8
		elif num_of_players == 3:
			num_cards_to_deal = 6
		else num_of_players >= 4:
			num_cards_to_deal = 5
		for card_index in range(0, num_cards_to_deal):
			for player in players:
				player.dealTo(self.game_deck.pop())
		for index, card in enumerate(reversed(self.game_deck)):
			if self._isCardANormalCard(card):
				self.played_deck.append(self.pickACard(index))
				break


	# This sets who plays first
	def setFirstPlay(self, firstPlay):
		self._firstPlay_ = self.players[firstPlay]
		self.setCurrentPlayer(self._firstPlay)

	def getCurrentPlayer(self):
		return self.current_player

	def setCurrentPlayer(self, player):
		self.current_player = player
		self.game_state[self.current_player] = PlayerState.PLAYING

	# This accepts a list
	# Stackable means it needs to accept new cards
	def setCardsLastPlayed(self, cards):
		if isinstance(cards, list):
			self.cards_played_last = cards
		else:
			raise TypeError("The argument provided is not a list")

	def getNextTurn(self):
		"""	Get the next person to play."""
		index = self.players.index(self.current_player) + 1 % len(self.players)
		while True:
			next_player = self.players[index]
			if self.game_state[next_player] == PlayerState.PAUSED:
				return next_player
			index = index + 1 % len(self.players) 

	def pickACard(self, index=None):
		if index==None:
			return self.game_deck.pop()
		return self.game_deck.pop(index)

	def play(self):
		"""
			Decides based on the cards played what action to take
			- 
			- If a combo card, '?' and '->', set all the players state apart from
			the current player to GameState.PLAYED and set the current player state 
			to PlayerState.PAUSED.
			- Otherwise set current player state to PlayerState.PLAYED. 

			Separate the action from playing the game.
		"""
		while self.game_state[self.current_player] == PlayerState.PLAYING:
			if len(self.cards_played_last) == 1:
				# match the cards
				if self._doesCardMatch(self.cards_played_last[0]):
					# place the cards on the played deck
					self.played_deck.append(self.cards_played_last[0])
					# take action: ie look at the top of the played deck
					if self._isCardANormalCard(self.played_deck[-1]):
						del self.cards_played_last[0]
						self.game_state[self.current_player] = PlayerState.PLAYED
						self.setCurrentPlayer(self.getNextTurn)
						break
					elif self._isCardAPickOneCard(self.cards_played_last[-1]):
							del self.cards_played_last[0]
							player_to_punish = self.getNextTurn()
							if not player.blocks():
								player_to_punish.pickOne()
							self.game_state[player_to_punish] = PlayerState.PLAYED
							self.game_state[self.current_player] = PlayerState.PLAYED
							self.setCurrentPlayer(self.getNextTurn)
							break
					elif 




	
	""" Private functions """

	# Checks
	def _isCardAPickOneCard(self, card):
		if isinstance(card, SpecialCard):
			return card.char == '1'

	def _isCardAPickTwoCard(self, card):
		if isinstance(card, SpecialCard):
			return card.char == '2'

	def _isCardAQuestionCard(self, card):
		if isinstance(card, SpecialCard):
			return card.char == '?'

	def _isCardASkipCard(self, card):
		if isinstance(card, SpecialCard):
			return card.char == '->'	
		
	def _isCardADropCard(self, card):
		if isinstance(card, SpecialCard):
			return card.char == '-'	

	def _isCardANormalCard(self, card):
		return isinstance(card, NormalCard)

	def _doesCardMatch(self, card):
		if isinstance(card, NormalCard):
			return any(card.shape == self.played_deck[-1].shape,
						card.colour == self.played_deck[-1].colour)
		elif isinstance(card, SpecialCard):
			return any(card.char == self.played_deck[-1].char,
						card.colour == self.played_deck[-1].colour)

	# Deck methods
	def _initSpecialCardDeck(self):
		special_card_deck = []
		for colour in self.colours:
			pick_one_card = SpecialCard(colour, CardColour.WHITE,'1', True, True)
			special_card_deck.append(pick_one_card)
			pick_two_card = SpecialCard(colour, CardColour.WHITE,'2', True, True)
			special_card_deck.append(pick_two_card)
			question_card = SpecialCard(colour, CardColour.WHITE, '?')
			special_card_deck.append(question_card)
			right_arrow_card = SpecialCard(colour, CardColour.WHITE, '->')
			special_card_deck.append(right_arrow_card)
			minus_card = SpecialCard(colour, CardColour.WHITE, '-')
			special_card_deck.append(minus_card)
		return special_card_deck

	def _initNormalCardDeck(self):
		return [[NormalCard(CardColour.BLACK, colour, shape) for colour in \
					self.colours for shape in self.shapes] for i in range(0, 5)]

	def _shuffleGameDeck(self):
		if len(self.game_deck) == 1:
			end = len(self.played_deck) - 1
			temp_list = [self.played_deck.pop(index) for index in range(0, end)]
			shuffle(temp_list)
			self.game_deck.extend(temp_list) 

def main():
	"""
	Initialise players and game

	:returns: A new game object and the first person to play
	"""
	players = []
	prompt()
	num_of_players = int(input("Enter the number of players playing the game: "))
	while(num_of_players < 2 or num_of_players > 8):
		print("You must have between 2 - 8 players(inclusive) playing this game ")
		num_of_players = int(input("Enter the number of players playing the game: "))
	for num in num_of_players:
		player_name=input("Enter your player name: ")
		players.append(Player(player_name))
	new_game = DiscardGame(players)
	person_to_play = input("Which player plays first? ")
	for player in players:
		if player.getNickname() == person_to_play:
			new_game.setFirstPlay(player)
			break
	return new_game, person_to_play

			







		






				



		