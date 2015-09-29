# This is the main file where
# input code is sent for interpretation
# and results/errors are outputted.

import os
import evaluation

def main():
    with open("test.txt", "r") as codefile: # read the code file
        text = codefile.read().strip()
    if not text:
        return
    eval = evaluation.Evaluater(text) # create code evaluater
    eval.begin() # begin interpretation

if __name__ == '__main__':
    main()