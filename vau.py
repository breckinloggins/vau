__author__ = 'bloggins'

import sys


def main():

    print "vau: a lisp. (type #quit to quit)"
    while 1:
        print "vau> ",
        input_line = sys.stdin.readline().rstrip('\n')
        if input_line == "#quit":
            break

        print "INPUT: %s" % input_line

if __name__ == "__main__":
    main()
