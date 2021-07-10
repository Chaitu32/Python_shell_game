def sign(x):
    if x==0:
        return 0
    return x/abs(x)

class ball:

    def __init__(self,x,y):
        self._x = x
        self._y = y-1
        self._ybase = y-1
        self._xspeed = 0
        self._yspeed = -2
        self._stick = True
        self._frames = 0
        self._gameover = False

    def _predict_hity(self,x_pad):
        new_y = self._y+sign(self._yspeed)
        if new_y==0:
            self._yspeed = -1* self._yspeed
            new_y = 1
        elif new_y==self._ybase+1:
            if self._x<x_pad+3 and self._x>x_pad-3:
                self._yspeed = -1* self._yspeed
                self._xspeed = self._x - x_pad +self._xspeed
                if self._xspeed>10:
                    self._xspeed = 10
                new_y = self._ybase
            else:
                self._gameover = True
        return new_y

    def _predict_hitx(self,max_x):
        new_x = self._x+sign(self._xspeed)
        if new_x<0:
            self._xspeed = -1* self._xspeed
            new_x = 0
        elif new_x==max_x+1:
            self._xspeed = -1* self._xspeed
            new_x = max_x
        return new_x

    # def is_hit(self,matix,old_x,old_y):
    #     ch = matix[self._y][self._x]
    #     ver = '|'.encode('utf-8')
    #     hor = '_'.encode('utf-8')
    #     if ch==ver:
    #         if matix[self._y][old_x]==hor:
    #             self._yspeed= -1*self._yspeed
    #             self._y = old_y
    #         else:
    #             self._xspeed = -1*self._xspeed
    #             self._x = old_x
    #     elif ch==hor and self._y!=self._ybase+1:
    #         self._yspeed = -1*self._yspeed
    #         self._y = old_y
    #     return self._x,self._y

    def update_fromhit(self,x,y):
        self._x = x
        self._y = y

    def reflec_y(self):
        self._yspeed = -1*self._yspeed

    def reflec_x(self):
        self._xspeed = -1*self._xspeed


    def update_pos(self,x_pad,max_x):
        old_x,old_y = (self._x,self._y)
        if self._stick==True:
            self._x = x_pad
            self._y = self._ybase
        else:
            if self._xspeed!=0:
                tempx = int(10/abs(self._xspeed))
                if self._frames%tempx==0:
                    self._x = int(self._predict_hitx(max_x))
            if self._yspeed!=0:
                tempy = int(10/abs(self._yspeed))
                if self._frames%tempy==0:
                    self._y = int(self._predict_hity(x_pad))
            self._frames += 1
            if self._frames%10==0:
                self._frames = 0
        return old_x,old_y

    def unstick(self):
        self._stick = False

    def reset_pad(self,x_pad,max_x):
        self._stick = True
        self._gameover = False
        self._xspeed = 0
        self._yspeed = -2
        self.update_pos(x_pad,max_x)

    def game_check(self):
        return self._gameover

    def __call__(self):
        return self._x,self._y

# temp = ball(2,10)
# print(temp())
# print(type(temp()[0]))