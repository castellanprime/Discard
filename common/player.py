import logging

class Player(object):
	
	def __init__(self, nick):
		self._logger = logging.getLogger(__name__)
		self.nick= nick
		self.deck = []
		self.last_played = []
		self.game = None
		self.last_card = False

	# This allows the player to join a game
	def join(self, game):
		self.game = game 
		self._logger.info("Joined game")

	def get_nick_name(self):
		return self.nick

	def get_deck(self):
		return self.deck

	def get_last_played(self):
		return self.last_played

	# This is the card numbers to remove
	# Refactor to allow for the players to retract their card/mistakes
	# This ability should be the given to the game
	def select_cards(self, card_numbers):
		self.last_played = [self.deck.pop(card_number) for card_number in card_numbers]
		if len(self.deck) == 1:
			self.last_card = True

	def add_a_card(self, card):
		self.deck.append(card)

	def pick_one(self, card):
		self.deck.insert(0, card)

	def give_up_turn(self):
		#self.pick_one()
		#self.game.set_current_player(self.game.get_next_turn())
		pass




	