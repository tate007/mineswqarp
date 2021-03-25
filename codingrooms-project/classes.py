from pydraw import *

class Menu_button:
    def __init__(self,screen,x,y,txt,txt_size=16):
        self.text = Text(screen,txt,x,y,size=txt_size,color=Color("white"),bold=True)
        self.rect = Rectangle(screen,x-txt_size,y-.5*txt_size,2*txt_size+self.text.width(),txt_size+self.text.height(),border=Color("white"),fill=False)

    def contains(self,location):
        if self.rect.contains(location):
            return True
        return False
    
    def center(self,location):
        self.text.center(location)
        self.rect.center(location)
    
    def move(self,x,y):
        self.text.move(x,y)
        self.rect.move(x,y)


class Tile:
    def __init__(self,screen,x,y,size):
        self.x = x
        self.y = y
        self.size = size

        self.covered_color = Color(189, 189, 189)
        self.uncovered_color = Color(119,119,119)

        self.rect = Rectangle(screen,x,y,size,size,color=Color(189, 189, 189),border=Color("black"),visible=False)
        # self.bomb_image = Image(screen,"bomb.png",x,y,size,size,visible=False)
        # self.flag_image = Image(screen,"red-flag-icon-13.jpg",x,y,size,size,visible=False)

        self.text = Text(screen,"",x,y,color=Color("white"))

        self.indices_in_range = []
        self.bombs_in_range = 0

        self.flagged = False
        self.uncovered = False
        self.bomb = False

    def flag(self):
        if not self.uncovered:
            if not self.flagged:
                self.flagged = True
                self.rect.color(Color("red"))
            else:
                self.flagged = False
                self.rect.color(self.covered_color)
                
    def contains(self,location):
        if self.rect.contains(location):
            return True
        return False
        
    def make_bomb(self):
        self.bomb = True

    def make_num(self):
        if self.bombs_in_range != 0:
            self.text.text(str(self.bombs_in_range))
            self.text.center(self.rect.center())


    def click(self):
        if not self.flagged:
            if not self.bomb:
                self.rect.color(self.uncovered_color)
                self.make_num()
                self.uncovered = True
        else:
            return False
    
    def reset(self):
        self.rect.color(self.covered_color)
        self.bomb = False
        self.uncovered = False
        self.flagged = False
        self.bombs_in_range = 0
        self.text.text("")