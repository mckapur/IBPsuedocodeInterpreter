# This file is the interpreter's lexical
# analyzer - it converts text code characters
# into different "tokens" and fetches them.

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
TokenTypes = Enum(['INT', 'PLUS', 'END'])

class Token: # a single "token" object
	def __init__(self, type, value):
		self.type = type # the "type" of the token, eg. integer
		self.value = value # the value of the token, eg. 5

	def __str__(self): # a token as a string; unique for each type-value pair
		return 'Token(' + self.type + ', ' + repr(self.value) + ')'

	def join(self, partner): # returns a boolean if the token could join the partner
		# we can only join in specific conditions:
		joined = False
		if partner.type == self.type:
			if self.type == TokenTypes.INT:
				self.value = self.value * 10 + partner.value
				joined = True
		return joined

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
		if token.type == TokenTypes.END: # if we are before the end, return
			if not self.currentToken.type == TokenTypes.END: # if we still have a current token to issue, don't end yet
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
		type = None
		value = None
		# evaluate type and value 
		if char.isdigit(): # it's an integer (NOTE: has to be an integer since it's just one character)
			type = TokenTypes.INT
			value = int(char)
		else: # it's a letter
			if char == '+':
				type = TokenTypes.PLUS
				value = char
		# Use type to convert to value
		return (type, value)