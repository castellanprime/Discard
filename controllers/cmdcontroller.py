"""
	This module is the controller class for the
	command-line version of Discard(Tm)
"""

class Controller(object):

	def __init__(self, views, game):
		self.views= views
		self.game = game
		self.new_game, self.person_to_play = self.game.main()

	def main(self):
		"""
		Start Game

		"""
		choice = 0
		while choice != 7:
			self.view[0].prompt()
			player = self.new_game.getCurrentPlayer()
			player.checkCards()
			st= "Player " + players.index(self.person_to_play) + ": What is your move"
			choice = int(input(st))
			if choice == 1:
				self.views[1].pretty_help()
			elif choice == 2:
				self.views[0].cmd_rules()
			elif choice == 3:
				player.checkCards()
				num_of_choices = int(input("How many cards are you choosing (1-2): "))
				while num_of_choices < 1 or num_of_choices > 2:
					print("Your answer has to either 1 or 2")
					num_of_choices = int(input("How many cards are you choosing (1-2): "))
				if num_of_choices == 1:
					card_one = input("Choose your card(the number): ")
					player.selectCards([card_one])
				elif num_of_choices == 2:
					st = "Choose your cards(the numbers)" +
							"[Order: firstCard, second Card]: "
					card_one, card_two = input(st)
					player.selectCards([card_one, card_two])
				player.play()
			elif choice==4:
				player.block()
			elif choice==5:
				player.giveUpTurn()
			elif choice==6:
				self.views[0].prompt()