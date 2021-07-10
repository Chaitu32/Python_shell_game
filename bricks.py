import numpy as np
from random import randint

class bricks:

    def __init__(self,level):
        self._arr = np.chararray((5))
        self._arr = ['|','_','_','_','|']
        self._level = level
        self._rainbow = False
        if self._level == 5:
            self._rainbow = True
            self._level = randint(0,3)


    def brick_hit(self):
        if self._rainbow==True:
            self._rainbow = False
        else :
            if self._level>0 and self._level<4: 
                self._level = self._level -1
            if self._level==0:
                self._arr = [' ',' ',' ',' ',' ']

    def level(self):
        if self._rainbow == True:
            self._level = ((self._level+1)%3)+1
        return self._level

    def __call__(self):
        return self._arr
