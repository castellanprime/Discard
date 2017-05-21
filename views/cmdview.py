"""
 	The module is the view class for the command-line version
 	of the Discard game

 	TODOs:
 		So far, none
"""
import textwrap

def menu():
	""" Menu options"""
	st="""

Welcome to the Discard(Tm).

Menu Options:
Select the number associated with action.
	1. about - Display more information about the game
	2. help - Display instructions
	3. play - play your turn
	4. block - block an action('1' or '2')
	5. pass - pass up your turn
	6. menu - show menu
	7. quit - exit
	"""
	dendented_text = textwrap.dedent(st).strip()
	print(dendented_text)

def rules():

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
	print(dendented_text)
