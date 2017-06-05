from enums import PlayerState
class PlayStates(object):

	"""Superclass for playing states of Discard"""
	def evaluate(self, discardGame, playedCards):
		raise NotImplementedError
	def __str__(self):
		return self.__doc__


class BeginPlayState(PlayStates):
	"""Initial beginning state"""
	def evaluate(self, discardGame, playedCards):
		if discardGame.do_cards_match(playedCards, discardGame._controller.get_top_card()):
			if discardGame.is_card_a_normal_card(playedCards):
				discardGame.update(playedCards)
				discardGame.update_state(self.__class__.__name__)
				discardGame.playing.player_state = PlayerState.PLAYED
				discardGame._controller.set_current_player()
				return None
			elif any(discardGame.is_card_a_pick_one_card(playedCards), 
				discardGame_is_card_a_pick_two_card(playedCards))
				return PickCardsState() 
			elif discardGame.is_card_a_question(playedCards):
				return QuestionCardState()
			elif discardGame.is_card_a_drop(playedCards):
				return DropCardState()
			elif discardGame.is_card_a_skip(playedCards):
				return SkipCardState()
		else:
			return PunishWrongMatchesState()


def PunishWrongMatchesState(PlayStates):
	""" Punishment for wrong card matches """
	def evaluate(self, discardGame, playedCards):
		discardGame.update(playedCards)
		discardGame.update_state(self.__class__.__name__)
		discardGame._controller.punish_for_wrong_match(discardGame._controller.current_player)
		discardGame.playing.player_state = PlayerState.PLAYED
		discardGame._controller.set_current_player()
		return None

def PickCardsState(PlayStates):
	""" Pick One or Pick Two Rules """
	def evaluate(self, discardGame, playedCards):
		if playedCards is None:
			# Non-blocking
			if all(discardGame.is_card_a_pick_one_card(playedCards),
				discardGame.is_a_pick_one_card(discardGame._controller.get_top_card())):
				for i in range(discardGame.num_of_pick_cards):
					discardGame.pick_one()
			if all(discardGame.is_card_a_pick_two_card(playedCards),
				discardGame.is_card_a_pick_two(discardGame._controller.get_top_card())):
				for i in range(discardGame.num_of_pick_cards):
					discardGame.pick_two()			
		else:
			# Blocking
			discardGame.num_of_pick_cards += 1
			discardGame.update(playedCards)
		discardGame.update_state(self.__class__.__name__)
		discardGame.playing.player_state = PlayerState.PLAYED
		discardGame._controller.set_current_player()
		return None

def QuestionCardState(PlayStates):
	""" Question Card Rules """
	def evaluate(self, discardGame, playedCards):
		if discardGame.is_card_a_question_card(discardGame._controller.get_top_card()) is False:
			discardGame.update(playedCards)
			discardGame.update_state(self.__class__.__name__)
			return self
		else:
		 	if playedCards is None:		# If it is  not combinable
				request_type, requested_card = discardGame._controller.request_a_card()
				player = discardGame._controller.get_next_player()
				request = request_type + requested_card
				card_choice = discardGame._controller.request_a_card_from_player(request, player)
				while card_choice[0] is None:
					discardGame._controller.deal_to_player(player)
					discardGame_controller.set_player_state(player, PlayerState.PLAYED)
					player = discardGame._controller.get_next_player(player)
					card_choice = discardGame._controller.request_a_card_from_player(request, player)
				discardGame.update(card_choice[0])
				discardGame_controller.set_player_state(player, PlayerState.PLAYED)
				discardGame.playing.player_state = PlayerState.PLAYED
				discardGame.update_state(self.__class__.name__)
				discardGame._controller.set_current_player()
				return None
			elif playedCards:
				if discardGame.is_card_a_drop(playedCards):
					return QuestionCardandDropCardState()
				elif discardGame.is_card_a_skip(playedCards):
					return QuestionCardandSkipState()
				elif any(discardGame.is_card_a_pick_two(playedCards),
					discardGame.is_card_a_pick_one(playedCards)):
					return QuestionCardandPickState()
				else:
					return PunishWrongMatchesState()

def DropCardState(PlayStates):
	""" Drop Card Rules """
	def evaluate(self, discardGame, playedCards):
		pass

def SkipCardState(PlayStates):
	""" Skip Card Rules """
	def evaluate(self, discardGame, playedCards):
		pass

def BlockState(PlayerStates):
	""" Rules for Blocking """
	def evaluate(self, discardGame, playedCards):
		if  any(all(discardGame.is_card_a_pick_one_card(playedCards),
			discardGame.is_a_pick_one_card(discardGame._controller.get_top_card())),
			all(discardGame.is_card_a_pick_two_card(playedCards),
			discardGame.is_card_a_pick_two(discardGame._controller.get_top_card())))
			return PickCardsState()
		return PunishWrongMatchesState() 

		
def QuestionCardandDropCardState(PlayerStates):
	""" Rules for combining a question card and a drop card """
	def evaluate(self, discardGame, playedCards):
		pass

def QuestionCardandPickState(PlayerStates):
	""" Rules for combining a question card and a pickone/picktwo card """
	def evaluate(self, discardGame, playedCards):
		pass

def QuestionCardandSkipState(PlayerStates):
	""" Rules for combining a question card and a skip card """
	def evaluate(self, discardGame, playedCards):
		pass



