# This file is the interpreter's evaluater -
# it uses a lexer to retrieve tokens, and
# then does operations with those tokens
# to produce the desired result

import lexer as lex

class Evaluater:
	def __init__(self, text):
		self.text = text # text to lex!
		self.lexer = lex.Lexer(self.text) # initialize the lexer
		self.currentTokenStream = []
	def begin(self):
		end = False
		while not end: # runs until told to end: which is an END token
			token = self.lexer.advanceCursor() # retrieve a new token
			end = (lex.TokenTypes.label(token.type) == lex.PROGRAMTERMINATOR) # end if there's a program terminator
			if lex.TokenTypes.label(token.type) == lex.LINETERMINATOR or end:
				self.evaluateTokenStream(self.currentTokenStream) # evaluate the current token stream only when we reach a line terminator
				self.currentTokenStream = [] # clear the token stream now that we have interpreted a line of code
			else:
				self.currentTokenStream.append(token) # add to the token stream
	def evaluateTokenStream(self, tokenStream):
		# operator is optional
		narrowedStream = self.narrowRecursively(tokenStream, 0) # narrow a stream of tokens to an underlying left hand side, right hand side, and optional operator
		if isinstance(narrowedStream[2], list): # if narrowed stream has a rhs stream, then we must separate into multiple commands
			toExecute = self.separateRecursively(tokenStream)
			for i in xrange(len(toExecute)):
				self.execute(toExecute[i])
		else:
			self.execute(narrowedStream)
	def narrowRecursively(self, tokenStream, cursor):
		# recursively narrow a token stream into a stream of an underlying lhs, rhs, and operator
		lhs = None
		opr = None
		rhs = None
		return (lhs, opr, rhs)
	def separateRecursively(self, tokenStream, cursor): # separate a command with multiple parameters into multiple commands by some arbitrary parameter delimeter
		return None
	def execute(self, tokenStream):
		lhs = tokenStream[0]
		opr = tokenStream[1]
		rhs = tokenStream[2]
		interval = None # the intermediate value to potentially store to or reference
		print tokenStream
		# real = actual value, we transform into no longer a token reference, but we have an assign location in any case for assignment operators
		realLhs = lhs.realValue()
		realRhs = rhs.realValue()
		assignLoc = None # TODO
		if opr:
			if opr.type == lex.TokenTypes.PLUS:
				interval = realLhs + realRhs
			if opr.type == lex.TokenTypes.MINUS:
				interval = realLhs - realRhs
			if opr.type == lex.TokenTypes.MULTIPLY:
				interval = realLhs * realRhs
			if opr.type == lex.TokenTypes.DIVIDE:
				interval = float(realLhs)/float(realRhs)
		return interval