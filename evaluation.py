# This file is the interpreter's evaluater -
# it uses a lexer to retrieve tokens, and
# then does operations with those tokens
# to produce the desired result

import lexer as lex

class Evaluater:
	def __init__(self, text):
		self.text = text # text to lex!
		self.lexer = lex.Lexer(self.text) # initialize the lexer
	def begin(self):
		end = False
		while not end: # runs until told to end: which is an END token
			token = self.lexer.advanceCursor() # retrieve a new token
			if token.type == lex.TokenTypes.END:
				end = True
			print token