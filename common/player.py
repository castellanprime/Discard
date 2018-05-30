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
		sstrs = "Joined game - " + self.nick
		self._logger.info(sstrs)

	def get_nick_name(self):
		return self.nick

	def get_deck(self):
		return self.deck

	def get_last_played(self):
		return self.last_played

	def select_cards(self, card_numbers):
		self.last_played = [self.deck.pop(card_number) for card_number in card_numbers]
		sstr = "The length of the deck: " + str(len(self.deck))
		self._logger.info(sstr)
		"""
		if len(self.deck) == 1:
			self.last_card = True
		elif len(self.deck) == 0:
			self.has_played_last_card = True
		"""

	def set_last_card(self):
		if self.last_card == False:
			self.last_card = True

	def has_played_last_card(self):
		return self.last_card

	def add_a_card(self, card):
		self.deck.append(card)

	def pick_one(self, card):
		self._logger.info(str(card))
		self.deck.insert(0, card)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.deck == other.deck and self.nick == other.nick and self.last_played == other.last_played
		return False

	def __ne__(self, other):
		return self.deck != other.deck or self.nick != other.nick or self.last_played != other.last_played

	def __hash__(self):
		return hash(self.nick)

	def __str__(self):
		return "Player: {}".format(self.nick)