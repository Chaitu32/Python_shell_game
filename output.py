import sys
import termios
import struct
import fcntl
import time
import numpy as np
from os import system
from colorama import init
from input import Get,input_to
from board import Board
from bricks import bricks
from ball import ball

colours = {
    0: '\033[49m',
    1: '\033[41m',
    2: '\033[42m',
    3: '\033[44m',
    4: '\033[43m',
    5: '\033[49m'
}

init()

class display(list):

    def __init__(self):
        self.height, self.width = struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, '1234'))
        self.height -=1
        self._matix = np.chararray((self.height,self.width),itemsize=2)
        self._matix[:] = ' '
        self._matix[0:1] = '_'
        self._matix[-1:] = '_'
        self._pad = Board(self._matix[-1:])
        self._max_steps = int((self.width-(int(self.height/2)*2))/7)
        self._brickpos = []
        self._level = 1
        for i in range(0,int(self.height/2)):
            temp = []
            for j in range(0,self._max_steps):
                temp.append(bricks(j%5+1))
            self._brickpos.append(temp)
        self._ball = ball(self._pad.center_pos(),self.height-1)
        self._score = 0
        self._lives = 3
        self._start_time = time.time()

    #Updates matix, Increases score and updates bricks
    def update_mat(self):
        temp = self._pad()
        self._matix[-1,:] = temp
        x_ball,y_ball = self._ball.update_pos(self._pad.center_pos(),self.width-1)
        prcx_ball,prcy_ball = self._ball()
        newx_ball,newy_ball = self._is_hit(x_ball,y_ball,prcx_ball,prcy_ball)
        if not (prcx_ball==newx_ball and prcy_ball==newy_ball):
            temp = self._brickpos[prcy_ball-1][int((prcx_ball-((prcy_ball-1)*2))/7)]
            temp.brick_hit()
            self._score +=10
            self.set_bricks()
        self._matix[y_ball][x_ball] = ' '
        self._matix[newy_ball][newx_ball] = 'O'
        #print(self._matix[-1:])

    #Reflection Handling function
    def _is_hit(self,old_x,old_y,new_x,new_y): 
        ch = self._matix[new_y][new_x]
        ver = '|'.encode('utf-8')
        hor = '_'.encode('utf-8')
        if ch==ver:
            if old_y==new_y:
                self._ball.reflec_x()
                new_x = old_x
            else:
                self._ball.reflec_y()
                new_y = old_y
        elif ch==hor and new_y!=self.height-1:
            if self._matix[old_y][new_x]==ver:
                self._brickpos[old_y-1][int((new_x-((old_y-1)*2))/7)].brick_hit()
                self._ball.reflec_x()
                new_x = old_x
            self._ball.reflec_y()
            new_y = old_y
        self._ball.update_fromhit(new_x,new_y)
        return new_x,new_y

    #Sets the layout of bricks
    def set_bricks(self):
        for i in range(0,int(self.height/2)):
            for h in range(0,self._max_steps):
                temp = self._brickpos[i][h]()
                for j in range(i*2+h*7,i*2+5+h*7):
                    self._matix[i+1][j] = temp[j-i*2-h*7]

    def movl(self):
        self._pad.move_left()

    def movr(self):
        self._pad.move_right()

    def start(self):
        self._ball.unstick()

    #Checks weather bricks are cleared or not
    def game_check(self):
        check = True
        for j in self._brickpos:
            for i in j:
                if i.level()!=0 and i.level()!=4:
                    check = False
                    break
        return (self._life_check() or check)

    #Checks life chances of ball
    def _life_check(self):
        if self._ball.game_check()==True:
            self._lives = self._lives -1
            self._pad.reset()
            x_pad = self._pad.center_pos()
            self._ball.reset_pad(x_pad,self.width-1)
        if self._lives <=0:
            return True
        return False

    #fetches score
    def get_score(self):
        return self._score

    #Converts Matix into string and adds colour to bricks.
    def __str__(self):
        s = []
        i = 0
        for row in self._matix:
            row = row.decode('utf-8')
            temp = ''.join(row)
            if i>0 and i<int(self.height/2)+1:
                start = (i-1)*2
                index = start
                temp2 = temp[:start]
                for j in range(0,self._max_steps):
                    temp2 += temp[start:index]+colours[self._brickpos[i-1][j].level()]+temp[index:index+5]+colours[5]
                    start = index+5
                    index = index+7
                temp2 += temp[start:]
                temp = temp2
            s.append(temp)
            i = i+1
        time_in_secs = time.time()-self._start_time
        score_card = "Score: "+str(self._score)+"<----->"+"Lives left: "+str(self._lives)+"<----->"+"Time: "+str(int(time_in_secs))
        s.append(score_card)
        string = '\n'.join(s)
        return string

    def print_bricks(self):
        print(self._brickpos[0])
        print(self._brickpos[1])