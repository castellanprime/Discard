"""
 	The module is the view class for the command-line version
 	of the Discard game

 	TODOs:
 		So far, none
"""
import textwrap

viewerrors = {
	1:"You can only pick one card at a time!!!",
	2:"You have no cards that you can use to block!!",
	3:"The card is not blockable",
	4:"That card is not a Normal Card",
	5:"That color is not allowed",
	6:"That shape is not allowed",
	7:"Cant not recognize option!!",
	8:"Card does not match!!",
	9:"There is no choice like that",
}

viewprompts = {
	1:"How many players are playing today?(Numbers):  ", 
	2:"Enter your player name: ",
	3:"Who wants to go first?: ",
	4:"Choose your card(the number): ",
	5:"Choose your option:",
	6:"Do you want to block?(y/n): ",
	7:"Do you want to combine with a card?(y/n): ",
	8:"What card do you want to combine with this card(the number)?: ",
	9:"What do you want to choose on colour or shape?(Colour/C/c or Shape/S/s): ",
	10:"What type of colour do you want(Red, Blue, Yellow, Green)?: ",
	11:"What type of shape do you want(Cross, Square, Triangle, Circle, Cup)?: ",
	12:"I am requesting this card: ",
	13:"Do you have the card requested, that is do you want to play that card(y/n)?: ",
	14:"Choose your cards(the numbers) [Order: firstCard, second Card]: ",
	15:"What Normal card do you want to ask for?(Enter 1 for shape, 2 for colour): ",
	16:"Do you have this colour?(y/n): ",
	17:"Bye, bye!!Enjoy the rest of your day",
	18:"Do you want to play a card or skip your turn?(Pick/Skip): "
}

def menu():
	""" Menu options"""
	st="""

Welcome to the Discard(Tm).

Menu Options:
Select the number associated with action.
	1. about - Display more information about the game
	2. help - Display instructions
	3. play - play your turn
	4. quit - exit
	"""
	dendented_text = textwrap.dedent(st).strip()
	print(dendented_text, "\n\n")

def cmd_rules():

	st="""
These are the rules for Discard(Tm). The numbers in 
the '' are the characters on the card faces.

'1' - 	Pick a card
'2' - 	Pick two cards
'?' - 	Ask for any Normal Card. If the player desires, the card can be
		accompanied by these cards with their effects
		-'->': Skip everybody and play again
		-'1': Everybody picks one card and you play again
		-'2': Everybody picks two cards and you play again
'-'	-	Discard any Normal Cards you have with it. If the player desires, 
		the card can be	accompanied by these cards with their effects
		-'1': The player discards one extra card.
		-'2': The player discards two extra cards.
		-'?': Remove a SpecialCard from the first player that has a Special Card.
		If there are no	special cards, the player can discard one extra card.
		-'->': Remove a SpecialCard from the next player in turn. If the player
		does not have a SpecialCard, the player can discard one extra card.
"""

	dendented_text = textwrap.dedent(st).strip()
	print(dendented_text, "\n\n")


def errors(num):
	return viewerrors[num]

def prompts(num):
	return viewprompts[num]

def display_cards(player_name, cards):
	if player_name:
		cards_rep = ','.join(["\n" + str(cards.index(card)) + ":" + repr(card) for card in cards])
		print("You:", player_name, " are playing", cards_rep)	
	else:
		print("Card to play against: ", cards)