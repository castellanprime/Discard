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
		print(first_play, " plays first")	
		choice = input("Do you want to change the direction of play?(y/n): ")
		if choice == 'y':
			players = self.model.get_players()
			players[:] = [val for val in reversed(players)]
			self.model.get_players()[:] = players
		else:
			print("You are keeping the default play")

		# Deals the cards to the players
		self.deal()
		while self.new_game.is_there_a_winner == False:
			self.main()

	def deal(self):
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
		print("Showing cards")
		for player in self.model.get_players():
			self.display_cards(player)

	def get_current_player(self):
		return self.current_player

	def pick_a_card(self, index):
		return self.model.get_a_card(index)

	def deal_to_player(self, player):
		player.add_a_card(self.pick_a_card()) 

	def request_a_card(self):
		choice = input(self.views[0].prompt(9))
		in_choice = ""
		while not any(choice.lower() == "colour", choice.lower == "s",
			choice.lower() == "shape", choice.lower() == "c"):
			print(self.views[0].errors(7))
			choice = input(self.views[0].prompt(9))
		if choice.lower() == "colour" or choice.lower() == "c":
			in_choice = input(self.views[0].prompt(10))
			while self.model.does_colour_exist(in_choice) is False:
				 in_choice = input(self.views[0].prompt(10))
			if self.model.does_colour_exist(in_choice):
				return "Colour:", in_choice
		if choice.lower() == "shape" or choice.lower() == "s":
			in_choice = input(self.views[0].prompt(11))
			while self.model.does_shape_exist(in_choice) is False:
				in_choice = input(self.views[0].prompt(10))
			if self.model.does_shape_exist(in_choice):
				return "Shape:", in_choice

	def get_last_player(self):
		return self.model.get_player_who_last_played()

	def request_a_card_from_player(self, request, player):
		print(self.views[0].prompt(12))
		choice = input(self.views[0].prompt(13))
		if choice == 'y':
			return (self.player_pick_a_card(player), 'y')
		return (None, 'n')

	def display_cards(self, player):
		cards = self.model.get_player_cards(player)
		self.views[0].display_cards(player.get_nick_name(), cards)

	# Is this necessary
	def display_player_cards(self, player):
		self.views[0].display_cards(player.get_nick_name(), player.get_deck())

	def player_pick_a_card(self, player):
		card = int(input(self.views[0].prompts(4)))
		while  card < 0  or card >= len(player.get_deck()):
			self.views[0].errors(1)
			card = int(input(self.views[0].prompts(4)))
		self.r_player_pick_a_card(card)

	def r_player_pick_a_card(self, index, player):
		player.select_cards([index])
		return player.get_last_played()

	def get_top_card(self):
		""" Get the last played card on the discard_pile"""
		return self.model.get_top_card()

	def display_top_card(self):
		self.views[0].display_cards(None, self.get_top_card())

	def get_player_state(self, player):
		return self.model.get_player_state(player)

	def set_player_state(self, player, state):
		self.model.set_player_state(player, state)

	def get_last_playing_state(self):
		return self.model.get_last_state()

	def punish_for_wrong_match(self, player):
		print(self.views[0].prompts(8))
		player.pick_one(self.pick_a_card())
		player.pick_one(self.pick_a_card())

	def get_next_turn(self, player=None):
		return self.model.get_next_turn(player)

	def set_current_player(self, player=None):
		self.current_player = self.model.set_current_player(self.get_next_turn(player).get_nick_name())

	def play_card(self, card):
		self.model.add_card(card)

	def update_state(self, state):
		self.model.add_state(state)

	def main(self):
		"""
		Start Game

		"""
		self.views[0].menu()
		choice = 0
		while choice != 4:
			self.views[0].menu()
			choice = int(input(self.views[0].prompts(5)))
			if choice == 1:
				self.views[1].pretty_help()
			elif choice == 2:
				self.views[0].cmd_rules()
			elif choice == 3:
				self.new_game.play1Round()
			elif choice < 1 or choice > 4:
				self.views[0].viewerrors(9)
		if choice == 4:
			sys.exit(1)


