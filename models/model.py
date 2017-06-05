"""
	This class contains the state of a game of Discard.
	That is:
	(a) who is currently playing
	(b) what hand is the player currently playing
	(c) what is left in the discard pile
"""

import logging
from collections import deque
from common.cards import NormalCard, SpecialCard
from common.enums import ShapeColour, CardColour, Shapes, PlayerState
from common.playerstate import State


class Model(object):

	def __init__(self):
		self._logger = logging.getLogger(__name__)
		self.discard_deck = []		  # Where all the cards played reside
		self.main_deck = []				# # Main game deck
		self.colours = [ShapeColour.RED, 
					ShapeColour.BLUE,
					ShapeColour.GREEN,
					ShapeColour.YELLOW]
		self.shapes = [Shapes.CROSS,
					Shapes.SQUARE,
					Shapes.TRIANGLE,
					Shapes.CIRCLE,
					Shapes.CUP]
		self._init_deck()
		self.last_played, self.current_player = None, None
		self.game_state = {}
		self.players = []
		self.state_history = []

	"Deck creation methods"
	def _create_special_card_deck(self):
		special_card_deck = []
		for colour in self.colours:
			pick_one_card = SpecialCard(colour, CardColour.WHITE,'1')
			special_card_deck.append(pick_one_card)
			pick_two_card = SpecialCard(colour, CardColour.WHITE,'2')
			special_card_deck.append(pick_two_card)
			question_card = SpecialCard(colour, CardColour.WHITE, '?')
			special_card_deck.append(question_card)
			right_arrow_card = SpecialCard(colour, CardColour.WHITE, '->')
			special_card_deck.append(right_arrow_card)
			minus_card = SpecialCard(colour, CardColour.WHITE, '-')
			special_card_deck.append(minus_card)
		return special_card_deck

	def _create_normal_card_deck(self):
		return [[NormalCard(CardColour.BLACK, colour, shape) for colour in \
					self.colours for shape in self.shapes] for i in range(0, 5)]

	def _init_deck(self):
		normal_deck = [card for deck in self._create_normal_card_deck() for card in deck]
		special_deck = self._create_special_card_deck()
		self.main_deck.append(normal_deck)
		self.main_deck.append(special_deck)
		self.main_deck[:] = [card for deck in self.main_deck for card in deck]
		self._logger.info("Created deck")

	def get_current_player(self):
		return self.current_player

	def get_player_who_last_played(self):
		return self.last_played

	def get_player_who_played_just_before(self, player):
		return self.get_last_turn(player)

	def find_player(self, player):
		for cur_player in self.players:
			if cur_player.get_nick_name() == player:
				self._logger.info("Found player")
				return cur_player

	def set_current_player(self, player):
		self.current_player = self.find_player(player)
		self._logger.info("Current player :", self.current_player.get_nick_name())
		self.game_state[self.current_player].player_state = PlayerState.PLAYING
		self.set_last_played()
		self.game_state[self.get_player_who_played_just_before(self.last_played)].player_state = PlayerState.PAUSED
		return self.current_player

	def set_last_played(self, player=None):
		self.last_played = self.get_last_turn(player)

	def get_game_deck(self):
		return self.main_deck

	def init_player_states(self):
		for player in self.players:
			self.game_state[player] = State(PlayerState.PAUSED, [])
			self._logger.info("Added player")

	def get_players(self):
		return self.players

	def get_player_cards(self, player):
		return self.players[self.players.index(player)].get_deck()

	def get_a_card(self, index):
		# Shuffle if the main_deck is small
		if len(self.main_deck) == 1:
			temp_list = deque(self.discard_deck)
			temp_deck = [temp_list.popleft() for index in range(0, len(temp_list)-1)]
			random.shuffle(temp_deck)
			self.main_deck.extend(temp_deck)
			self.discard_deck = list(temp_list)
		if index:
			return self.main_deck.pop(index)
		else:
			return self.main_deck.pop()

	def get_player_state(self, player):
		return self.game_state[player]

	def set_player_state(self, player, state):
		self.game_state[player].player_state = state

	def get_top_card(self):
		return self.discard_deck[-1]

	def get_next_turn(self, player=None):
		"""	Get the next person to play."""
		self._logger.info("Getting next player to play")
		_player = None
		if player:
			_player = player
		else:
			_player = self.current_player
		index = self.players.index(_player) + 1 % len(self.players)
		while True:
			next_player = self.players[index]
			if self.game_state[next_player] == PlayerState.PAUSED:
				return next_player
			index = index + 1 % len(self.players) 

	def get_last_turn(self, player=None):
		"""	Get the last person that played."""
		self._logger.info("Getting player who played before this player")
		_player = None
		if player:
			_player = player
		else:
			_player = self.current_player
		index = self.players.index(_player) - 1 % len(self.players)
		return self.players[index]


	def add_card(self, card):
		self.discard_deck.append(card)

	def add_state(self, state):
		self.state_history.append(state)

	def get_last_state(self):
		return self.state_history[-1]

	def does_shape_exist(self, shape):
		return shape.lower() in [val.name.lower() for val in self.shapes]

	def does_colour_exist(self, colour):
		return colour.lower() in [val.name.lower() for val in self.colours]

	def save(self):
		pass

	def retrieve(self):
		pass