import numpy as np

class typeboard:

    def __init__(self):
        self._type = np.chararray((5))
        self._type[:] ='I'

    def expand(self):
        self._type = np.chararr((self._type.shape[0]+2))
        self._type[:] ='I'

    def shrink(self):
        self._type = np.chararr((self._type.shape[0]-2))
        self._type[:] ='I'

    def bullets(self):
        self._type[0] = '^'
        self._type[-1] = '^' 



class Board(typeboard):

    def __init__(self,matix):
        super().__init__()
        self._row = matix.flatten()
        self._position = int(self._row.shape[0]/2)
        self._change_position(0)
    
    def _change_position(self,value):
        temp = self._position + value
        if temp-self._type.shape[0]/2 >= 0 and  temp+self._type.shape[0]/2 < self._row.shape[0]:
            self._position = temp
            i =0
            self._row[:] = '_'
            for x in range((self._position-int(self._type.shape[0]/2)),self._position+int(self._type.shape[0]/2)+1):
                self._row[x] = self._type[i]
                i +=1

    def move_left(self):
        self._change_position(-1)

    def move_right(self):
        self._change_position(1)

    def reset(self):
        self._position = int(self._row.shape[0]/2)
        super().__init__()
        self._change_position(0)

    def center_pos(self):
        return self._position

    def __call__(self):
        return self._row
