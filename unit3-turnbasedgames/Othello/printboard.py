import sys
board = sys.argv[1]

to_print = ''
for count, char in enumerate(board):
    if count % 8 == 0:
        to_print += '\n'
    to_print += char

print(to_print)