# This is the main file where
# input code is sent for interpretation
# and results/errors are outputted.

import evaluation

def main():
    while True:
        try:
            text = raw_input('Psuedocode> ')
        except EOFError:
            break
        if not text:
            continue
        eval = evaluation.Evaluater(text)
        eval.begin()

if __name__ == '__main__':
    main()