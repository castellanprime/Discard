"""
	This module contains the game logic/rules
	for Discard

"""
import logging
from common.cards import NormalCard, SpecialCard
from common.playstates import BeginPlayState, PickCardsState, QuestionCardState
from common.enums import PlayerState

class DiscardGame(object):

	def __init__(self, controller):
		self._controller = controller
		self._logger = logging.getLogger(__name__)
		self.state, self.playing = None, None
		self.played_cards = []
		self.num_of_pick_cards = 0
		self.is_there_a_winner = False			# If there is a winner
		#self.current_player, self._first_play = None, None
		#self.asked_card_colour, self.asked_card_shape = "", "" 
		#self.asked_for_cards = False
		#self.drop_cards = [False, 0]		# Number of cards to drop

	""" Checks """
	def is_card_a_normalcard(self, card):
		return isinstance(card, NormalCard)

	def is_card_a_specialcard(self, card):
		return isinstance(card, SpecialCard)

	def is_card_a_pickone(self, card):
		if self.is_card_a_specialcard(card):
			return card.char == '1'

	def is_card_a_picktwo(self, card):
		if self.is_card_a_specialcard(card):
			return card.char == '2'

	def is_card_a_question(self, card):
		if self.is_card_a_specialcard(card):
			return card.char == '?'

	def is_card_a_skip(self, card):
		if self.is_card_a_specialcard(card):
			return card.char == '->'	
		
	def is_card_a_drop(self, card):
		if self.is_card_a_specialcard(card):
			return card.char == '-'	

	def do_cards_match(self, card_one, card_two):
		self._logger.info("Do cards match")
		""" Checks if the card matches either
		(a)	Shape or Colour in the case of a normal card
		(b) Char or colour in the case of a special card
		"""
		if self.is_card_a_normalcard(card_one) and self.is_card_a_normalcard(card_two):
			return any((card_one.shape == card_two.shape,
						card_one.get_shape_colour() == card_two.get_shape_colour()))
		elif ((self.is_card_a_specialcard(card_one) and self.is_card_a_normalcard(card_two))
			or (self.is_card_a_normalcard(card_one) and self.is_card_a_specialcard(card_two))):
			return card_one.get_shape_colour() == card_two.get_char_colour()
		elif self.is_card_a_specialcard(card_one) and self.is_card_a_specialcard(card_two):
			return any((card_one.char == card_two.char,
						card_one.get_char_colour() == card_two.get_char_colour()))

	def play1Round(self):
		self.state = BeginPlayState()
		self.playing = self._controller.get_player_state(self._controller.current_player)
		while self.playing.player_state == PlayerState.PLAYING:
			self._controller.display_top_card()
			if ( any((self.is_card_a_pickone(self._controller.get_top_card()), 
				self.is_card_a_picktwo(self._controller.get_top_card()))) and 
				self._controller.get_last_playing_state() == "PickCardsState"):
				choice = input(self._controller.views[0].prompt(6))
				if choice == 'n':
					self.state = PickCardsState()
					self.state = self.state.evaluate(self, None)
				else:
					self._controller.display_cards(self._controller.current_player)
					self.played_cards = self._controller.player_pick_a_card(self._controller.current_player)
					self.state = BlockState()
					self.state = self.state.evaluate(self, self.played_cards)
			elif any((isinstance(self.state, QuestionCardState), 
					isinstance(self.state, DropCardState), 
					isinstance(self.state, SkipState))):
				choice = input(self._controller.views[0].prompt(7))
				if choice == 'y':
					self._controller.display_cards(self._controller.current_player)
					self.played_cards = self._controller.player_pick_a_card(self._controller.current_player)
					self.state = self.state.evaluate(self, self.played_cards)
				elif choice == 'n':
					self.state = self.state.evaluate(self, None)
			elif isinstance(self.state, QuestionCardandSkipState):
				return			# allows the player to play again
			else: 
				self._controller.display_cards(self._controller.current_player)
				self.played_cards = self._controller.player_pick_a_card(self._controller.current_player)
				self.state = self.state.evaluate(self, self.played_cards)

	def update(self, playedCards):
		self._controller.play_card(playedCards)

	def update_state(self, state):
		self._controller.update_state(state)
	
	def pick_one(self):
		self._controller.deal_to_player(self._controller.current_player)

	def pick_two(self):
		self.pick_one()
		self.pick_one()

	def win(self):
		pass

	def lose(self):
		pass

	


