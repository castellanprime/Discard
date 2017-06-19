"""
	This module contains the game logic/rules
	for Discard

"""
import logging
from common.cards import NormalCard, SpecialCard
from common.playstates import BeginPlayState, PickCardsState, QuestionCardState, \
		DropCardState, SkipCardState, QuestionCardandSkipState, NormalCardState, PunishWrongMatchesState
from common.enums import PlayerState

class DiscardGame(object):

	def __init__(self, controller):
		self._controller = controller
		self._logger = logging.getLogger(__name__)
		self.state, self.playing = None, None
		self.played_cards = None
		self.num_of_pick_cards = 0
		self.is_there_a_winner = False			# If there is a winner
		
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
		sstr = "Card_one: " + str(card_one) +  "\nCard_two: " + str(card_two) 
		self._logger.debug(sstr)
		if self.is_card_a_normalcard(card_one) and self.is_card_a_normalcard(card_two):
			return any((card_one.shape == card_two.shape,
						card_one.get_shape_colour() == card_two.get_shape_colour()))
		elif self.is_card_a_specialcard(card_one) and self.is_card_a_normalcard(card_two):
			return card_one.get_char_colour() == card_two.get_shape_colour()
		elif self.is_card_a_normalcard(card_one) and self.is_card_a_specialcard(card_two):
			return card_one.get_shape_colour() == card_two.get_char_colour()
		elif self.is_card_a_specialcard(card_one) and self.is_card_a_specialcard(card_two):
			return any((card_one.char == card_two.char,
						card_one.get_char_colour() == card_two.get_char_colour()))

	def play1Round(self):
		self.state = BeginPlayState()
		self.playing = self._controller.get_player_state(self._controller.current_player)
		while self.playing.player_state == PlayerState.PLAYING:
			self._controller.display_top_card()
			if ((self.is_card_a_pickone(self._controller.get_top_card()) or 
				self.is_card_a_picktwo(self._controller.get_top_card())) and 
				self._controller.get_last_playing_state() == "PickCardsState"):
					# For current player that has not played a pick one or pick two card
				choice = input(self._controller.views[0].prompts(6))	# Do he/she want to block
				if choice == 'n':
					self._logger.debug(str(self.state))
					self.state = PickCardsState()
					self.state = self.state.evaluate(self, None)
					self._logger.debug(str(self.state))
				else:
					self._logger.debug(str(self.state))
					self._controller.display_cards(self._controller.current_player)
					self.played_cards = self._controller.player_pick_a_card(self._controller.current_player)[0]	# Pick the blocking card
					self.state = BlockState()
					self.state = self.state.evaluate(self, self.played_cards)
					self._logger.debug(str(self.state))
			elif ((self.is_card_a_pickone(self._controller.get_top_card()) or  
				self.is_card_a_picktwo(self._controller.get_top_card())) and 
				self._controller.get_last_playing_state() != "PickCardsState"):
					# For current player that has just played a pick one or pick two card
					self._logger.debug(str(self.state))
					self.state = self.state.evaluate(self, self.played_cards)
					self._logger.debug(str(self.state))
			elif any((isinstance(self.state, QuestionCardState), 
					isinstance(self.state, DropCardState), 
					isinstance(self.state, SkipCardState))):
				choice = input(self._controller.views[0].prompts(7))
				self.update(self.played_cards)
				if choice == 'y':
					self._logger.debug(str(self.state))
					self._controller.display_cards(self._controller.current_player)
					self.played_cards = self._controller.player_pick_a_card(self._controller.current_player)[0]
					self.state = self.state.evaluate(self, self.played_cards)
					self._logger.debug(str(self.state))
				elif choice == 'n':
					self._logger.debug(str(self.state))
					self.state = self.state.evaluate(self, None)
					self._logger.debug(str(self.state))
			elif isinstance(self.state, QuestionCardandSkipState):
				return			# allows the player to play again
			elif any((isinstance(self.state, NormalCardState), 
				isinstance(self.state, PunishWrongMatchesState))):
					self._logger.debug(str(self.state))
					self.state = self.state.evaluate(self, self.played_cards)
					self._logger.debug(str(self.state))
			else: 
				# Normal play
				self._controller.display_cards(self._controller.current_player)
				pick_choice = self._controller.ask_to_pick()
				if pick_choice.lower() == "pick":
					self.played_cards = self._controller.player_pick_a_card(self._controller.current_player)[0]
					sstr = "You picked: " + str(self.played_cards)
					self._controller.display_message(sstr)
					self._logger.debug(sstr)
					st = "Starting the round: " + self.state.__class__.__name__
					self._logger.info(st)
					self.state = self.state.evaluate(self, self.played_cards)
					self._logger.debug(str(self.state))
				else:
					# If the player wants to skip his/her turn
					self._logger.info("Skipping turn")
					self.pick_one()
					self.playing.player_state = PlayerState.PLAYED
					self._controller.set_current_player()

			# Determine who won and end game
			if self._controller.get_last_player().has_played_last_card == True:
				self._controller.set_win_status(self._controller.get_last_player())
				self.is_there_a_winner = True
				return

	def update(self, playedCards):
		self._controller.play_card(playedCards)

	def update_state(self, state):
		self._controller.update_state(state)
	
	def pick_one(self):
		self._controller.deal_to_player(self._controller.current_player)

	def pick_two(self):
		self.pick_one()
		self.pick_one()