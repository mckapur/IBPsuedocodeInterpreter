# This file is the interpreter's lexical
# analyzer - it converts text code characters
# into different "tokens" and fetches them.

# TODO: Error Handling

import re as regex
import copy

ASSIGN = 'OPERATOR_ASSIGN' # assignment operator
INTEROP = 'OPERATOR_INTERMEDIATE' # not an assignment; any intermediate calculation or operation
FIXED_VALUE = 'FIXED_VALUE' # cannot assign FIVAL to anything
VARIABLE_VALUE = 'VARIABLE_VALUE' # can assign VARVAL to anything
LINETERMINATOR = 'LINETERMINATOR' # terminates a line of code
PROGRAMTERMINATOR = 'PROGRAMTERMINATOR' # terminates the program
COMMAND = 'COMMAND'
PARAMETERDELIMETER = 'PARAMETERDELIMETER' # a delimeter that can separate mutliple parameters to any command
CLAUSE = 'CLAUSE'
ARBITRARY = 'ARBITRARY'
class TokenTypeEnum(list):
	def __getattr__(self, name): # convenience method
		for i, val in enumerate(self):
			if val[0] == name:
				return name
		raise AttributeError
	def label(self, name): # get the label/grouping of the token type name
		for i, val in enumerate(self):
			if val[0] == name:
				return val[2]
		raise AttributeErrors
	def nameFromCharacter(self, char): # use regex to determine the type of token from the character
		for i, val in enumerate(self):
			if regex.match(val[1], char) is not None:
				return val[0]
		raise AttributeError

	# TODO: implement separate methods from variable_value name and _actual_ value in memory, realValue
# Token type tuple: (name, regex value, label/descriptor)
TokenTypes = TokenTypeEnum([('INT', '[0-9]', FIXED_VALUE), ('PLUS', '[+]', INTEROP), ('MINUS', '[-]', INTEROP), ('MULTIPLY', '[*]', INTEROP), ('DIVIDE', '[/]', INTEROP), ('ASSIGN', '[=]', ASSIGN), ('SPACE', '[ ]', ARBITRARY), ('DOT', '[.]', ARBITRARY), ('NEWLINE', '[\n]', LINETERMINATOR), ('COMMA', '[,]', PARAMETERDELIMETER), ('END', None, PROGRAMTERMINATOR)])

class Token: # a single "token" object
	def __init__(self, type, value):
		self.type = type # the "type" of the token, eg. integer
		self.value = value # the value of the token, eg. 5

	def __str__(self): # a token as a string; unique for each type-value pair
		return 'Token(' + self.type + ', ' + repr(self.value) + ')'

	def join(self, partner): # returns a boolean if the token could join the partner
		# we can only join in specific conditions:
		joined = False
		tempToken = copy.copy(self)
		if partner.type == self.type:
			if self.type == TokenTypes.INT:
				self.value = self.value * 10 + partner.value
			if self.type == TokenTypes.SPACE:
				self.value = ''.join([self.value, partner.value])
		elif (partner.type == TokenTypes.MINUS or self.type == TokenTypes.PLUS) and (self.type == TokenTypes.MINUS or partner.type == TokenTypes.PLUS):
			if partner.type == TokenTypes.MINUS:
				self.type = partner.type
				self.value = partner.value
		if not self.value == tempToken.value or not self.type == tempToken.type:
			joined = True
		return joined

	def realValue(self): # get the real value from a token type name, mostly useful for variable values
		# TODO
		return self.value 

	def __repr__(self):
		return self.__str__() # as it's unique for each type-value pair

class Lexer(object): # the lexer class
	def __init__(self, text):
		self.text = text # text to lex!
		self.cursor = 0 # currently expanded token index
		self.currentToken = None # the curent token we are evaluating

	def error(self):
		raise Exception("There was an error parsing the input")

	def expandNextToken(self): # evaluates the next character and expands the token
		if self.cursor > (len(self.text) - 1): # if there are no more characters to evaluate, then create an END token to end the program
			return Token(TokenTypes.END, None)
		tokenData = self.tokenDataFromCharacter(self.text[self.cursor]) # convert the current character to token data and use that to expand a token
		return Token(tokenData[0], tokenData[1])

	def advanceCursor(self):
		token = self.expandNextToken() # expand next token
		self.cursor += 1 # increment the counter
		if not self.currentToken: # if this is the first token, do not join (infinite loop: Tn join Tn == True)
			self.currentToken = token
			return self.advanceCursor()
		if TokenTypes.label(token.type) == PROGRAMTERMINATOR: # if we are at the end, return
			if not TokenTypes.label(self.currentToken.type) == PROGRAMTERMINATOR: # if we still have a current token to issue, don't end yet
				intermediateToken = self.currentToken
				self.currentToken = token
				return intermediateToken
			else:
				return self.currentToken # end of program
		if self.currentToken.join(token): # if the join was successful, advance the cursor again
			return self.advanceCursor()
		else:
			intermediateToken = self.currentToken
			self.currentToken = token
			return intermediateToken # if the join was not successful, return the token as is

	def tokenDataFromCharacter(self, char):
		type = TokenTypes.nameFromCharacter(char)
		value = char
		if type == TokenTypes.INT:
			value = int(char)
		# Use type to convert to value
		return (type, value)