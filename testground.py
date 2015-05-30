from ariadne.generators import *
import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python " + sys.argv[0] + " width height")
        sys.exit(1)

    width = int(sys.argv[1])
    height = int(sys.argv[2])

    print(RecursiveBacktracker().generate(width, height))
