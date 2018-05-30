"""
	This module is the controller class for the
	command-line version of Discard(Tm)
"""
import logging, random, sys
from common.game import DiscardGame
from common.player import Player
from models.model import Model

class Controller(object):

	def __init__(self, views):
		self._logger = logging.getLogger(__name__)
		self.views= views
		self.model = Model()
		self.new_game = DiscardGame(self)
		self.current_player = None
		self.winner = None
		self.state = None

	def start_game(self):
		""" Initialise a new game """
		# Adds new players
		num_of_players = int(input(self.views[0].prompts(1)))
		for num in range(num_of_players):
			print("Player " , num)
			player_name=input(self.views[0].prompts(2))
			player = Player(player_name)
			self.model.players.append(Player(player_name))
			player.join(self.new_game)
		self.model.init_player_states()
		first_play = input(self.views[0].prompts(3))
		self.current_player = self.model.set_current_player(first_play)
		while self.current_player is None:
			first_play = input(self.views[0].prompts(3))
			self.current_player = self.model.set_current_player(first_play)
		print(first_play, " plays first")	
		choice = input("Do you want to change the direction of play?(y/n): ")
		if choice == 'y':
			players = self.model.get_players()
			players[:] = [val for val in reversed(players)]
			self.model.get_players()[:] = players
		else:
			print("You are keeping the default play")

		print("Player order: ", ",".join([str(player) for player in self.model.get_players()]))
		
		# Deals the cards to the players
		self.deal()

		#If top card is a special card
		while self.new_game.is_card_a_specialcard(self.get_top_card()):
			self.deal(False)

		# While no one has won
		while self.new_game.is_there_a_winner == False:
			self.main()
		
		# Somebody has won
		ssstr = str(self.winner) + " has won"
		self.display_message(ssstr)
		sys.exit(0)

	def deal(self, deal_to_players=True):
		num_of_players = len(self.model.get_players())
		num_cards_to_deal = 0
		if num_of_players == 2:
			num_cards_to_deal = 8
		elif num_of_players == 3:
			num_cards_to_deal = 6
		else:
			num_cards_to_deal = 5
		temp_list = self.model.get_game_deck()
		random.shuffle(temp_list)
		self.model.main_deck[:] = temp_list
		for card_index in range(0, num_cards_to_deal):
			for player in self.model.get_players():
				player.add_a_card(self.pick_a_card(index=None))
		for index, card in enumerate(reversed(self.model.get_game_deck())):
			if self.new_game.is_card_a_normalcard(card):
				self.model.discard_deck.append(self.pick_a_card(index))
				break
		if deal_to_players:
			print("\nShowing cards")
			for player in self.model.get_players():
				self.display_cards(player)
			print("\n")

	def get_current_player(self):
		return self.current_player

	def get_num_of_players(self):
		return len(self.model.get_players())

	def force_player_to_play(self, player):
		self.model.force_player_to_play(player)

	def pick_a_card(self, index):
		return self.model.get_a_card(index)

	def deal_to_player(self, player):
		player.add_a_card(self.pick_a_card(None)) 

	def request_a_card(self):
		choice = input(self.views[0].prompts(9))
		in_choice = ""
		while not any((choice.lower() == "colour", choice.lower() == "s",
			choice.lower() == "shape", choice.lower() == "c")):
			print(self.views[0].errors(7))
			choice = input(self.views[0].prompts(9))
		if choice.lower() == "colour" or choice.lower() == "c":
			in_choice = input(self.views[0].prompts(10))
			while self.model.does_colour_exist(in_choice) is False:
				 in_choice = input(self.views[0].prompts(10))
			return "Colour:", in_choice
		if choice.lower() == "shape" or choice.lower() == "s":
			in_choice = input(self.views[0].prompts(11))
			while self.model.does_shape_exist(in_choice) is False:
				in_choice = input(self.views[0].prompts(10))
			return "Shape:", in_choice

	def get_last_player(self):
		return self.model.get_player_who_last_played()

	def get_next_player(self, player):
		return self.model.get_next_player(player)

	def request_a_card_from_player(self, request, player):
		print(str(player))
		self._logger.debug(str(player))
		print(self.views[0].prompts(12), request)
		choice = input(self.views[0].prompts(13))
		if choice == 'y':
			return (self.player_pick_a_card(player)[0], 'y')
		return (None, 'n')

	def set_win_status(self, player):
		self.winner = self.model.set_win_status(player)

	def display_cards(self, player):
		cards = self.model.get_player_cards(player)
		self.views[0].display_cards(player.get_nick_name(), cards)

	# Is this necessary
	def display_player_cards(self, player):
		self.views[0].display_cards(player.get_nick_name(), player.get_deck())

	def ask_to_pick(self, lastcard=False):
		while True:
			if lastcard:
				choice = input(self.views[0].prompts(22))
				if any(( choice.lower() == "pick",choice.lower() == "skip", 
					choice.lower() == "lastcard")):
					st = "You selected: " + choice
					self._logger.info(st)
					return choice.lower()
			else:
				choice = input(self.views[0].prompts(22))
				if any(( choice.lower() == "pick",choice.lower() == "skip")):
					st = "You selected: " + choice
					self._logger.info(st)
					return choice.lower()
			print(self.views[0].errors(10))	

	def player_pick_a_card(self, player):
		card = int(input(self.views[0].prompts(4)))
		while  card < 0  or card >= len(player.get_deck()):
			self.views[0].errors(1)
			card = int(input(self.views[0].prompts(4)))
		return self.r_player_pick_a_card(card, player)

	def r_player_pick_a_card(self, index, player):
		player.select_cards([index])
		st = "You picked:" + str(player.get_last_played())
		self._logger.info(st)
		return player.get_last_played()

	def get_top_card(self):
		""" Get the last played card on the discard_pile"""
		return self.model.get_top_card()

	def check_if_last_card(self):
		""" Set last card """
		return all((len(self.current_player.get_deck()) <= 2, self.current_player.has_played_last_card() == False))

	def display_top_card(self):
		self.views[0].display_cards(None, self.get_top_card())

	def get_player_state(self, player):
		return self.model.get_player_state(player)

	def set_player_state(self, player, state):
		self.model.set_player_state(player, state)

	def get_last_playing_state(self):
		return self.model.get_last_state()

	def punish_for_wrong_match(self, player):
		self.display_message(self.views[0].errors(8))
		self.display_message(self.views[0].prompts(19))
		player.pick_one(self.pick_a_card(None))
		player.pick_one(self.pick_a_card(None))

	def get_next_turn(self, player=None):
		return self.model.get_next_turn(player)

	def set_current_player(self, player=None):
		self.current_player = self.model.set_current_player(self.get_next_turn(player).get_nick_name())

	def play_card(self, card):
		self.model.add_card(card)

	def update_state(self, state):
		self.model.add_state(state)

	def display_message(self, sstr):
		self.views[0].display_message(sstr)

	def display_last_card_rules(self):
		self.display_message(self.views[0].prompts(21))

	def get_colour(self, col):
		return self.model.get_colour(col)[0]

	def get_shape(self, shap):
		return self.model.get_shape(shap)[0]

	def get_random_colour(self):
		return random.choice(self.model.colours)

	def get_random_shape(self):
		return random.choice(self.model.shapes)

	def main(self):
		"""
		Start Game

		"""
		choice = 0
		while choice != 4:
			self.views[0].menu()
			sstrs = "Currently playing " + str(self.current_player)
			self.display_message(sstrs)
			str_choice = input(self.views[0].prompts(5))
			while any((str_choice is None, not str_choice.strip())): 	# string is None or string is empty
				self.display_message(self.views[0].errors(11))
				str_choice = input(self.views[0].prompts(5))
			try:
				choice = int(str_choice)
			except ValueError as e:
				self.display_message(self.views[0].errors(12))
			else:
				if choice == 1:
					self.views[1].pretty_help()
				elif choice == 2:
					self.views[0].cmd_rules()
				elif choice == 3:
					self.new_game.play1Round()
					if self.new_game.has_someone_won() == True:
						st = self.get_last_player().get_nick_name() + " has won!!"
						self.display_message(st)
						sys.exit(0)
				elif choice < 1 or choice > 4:
					self.display_message(self.views[0].errors(9))
		if choice == 4:
			print(self.views[0].prompts(17))
			sys.exit(0)


