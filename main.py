import sys
import termios
import struct
import fcntl
import time
from os import system
from colorama import init
from input import Get,input_to
from output import display

def game():
    d = display()
    user_input = Get()
    d.set_bricks()
    while True:
        try:
            system('clear')
            d.update_mat()
            sys.stdout.write('%s' % d)
            sys.stdout.flush()
            if d.game_check()==True:
                score = d.get_score()
                sys.stdout.write('\r'+'\n\033[1m\033[32m=== Game Over And Score is %d ====\033[0m\n' % score)
                sys.exit()
            #time.sleep(0.05)
            try:
                ch = input_to(user_input)
                if ch=='a':
                    d.movl()
                elif ch=='d':
                    d.movr()
                elif ch=='w':
                    d.start()
                elif ch=='q':
                    exit()
            except KeyboardInterrupt:
                sys.stdout.write('\r'+'\n\033[1m\033[32m=== Game Stopped ====\033[0m\n')
                sys.exit()
        except KeyboardInterrupt:
            sys.stdout.write('\r'+'\n\033[1m\033[32m=== Game Stopped ====\033[0m\n')
            sys.exit()

game()