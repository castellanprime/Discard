class Card:

	def __init__(self, card_colour, other_colour):
		self.card_colour = card_colour
		self.other_colour = other_colour

	def __repr__(self):
		return "{0}:{1}".format(self.card_colour, self.other_colour)

class NormalCard(Card):

	def __init__(self, card_colour, shape_colour, shape):
		super().__init__(self, card_colour, shape_colour)
		self.shape = shape

	def __repr__(self):
		return "[{0} {1}]".format(self.shape, super().__repr__())

class SpecialCard(Card):

	def __init__(self, card_colour, char_colour, char, 
				is_blockable=False, is_stackable=False):
		super().__init__(self, card_colour, char_colour)
		self.char = char
		self.is_blockable = is_blockable
		self.is_stackable = is_stackable

	def __repr__(self):
		return "[{0} {1}]".format(self.shape, super().__repr__())