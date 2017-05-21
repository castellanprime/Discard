class Player(object):
	
	def __init__(self, nick):
		self.nick= nick
		self.deck = []
		self.last_played = []

	# This allows the player to join a game
	def join(self, game):
		self.game = game 

	def getNickname(self):
		return self.nick

	# This is the card numbers to remove
	# Refactor to allow for the players to retract their card/mistakes
	# This ability should be the given to the game
	def selectCards(self, card_numbers):
		self.last_played = [self.deck.pop(card_number) for card_number in card_numbers]
	
	def play(self):
		self.game.setCardsLastPlayed(self.last_played)
		self.game.play()

	def checkCards(self):
		return ','.join([str(self.deck.index(card)) \
				+ ":" + repr(card)) for card in self.deck])

	def pickOne(self):
		self.deck.append(self.game.pickACard())

	def pickTwo(self):
		self.pickOne()
		self.pickOne()

	def blocks(self):
		if self.game.played_deck[0] in self.deck:

	def giveUpTurn(self):
		self.pickOne()
		self.game.setCurrentPlayer(self.game.getNextTurn())


	