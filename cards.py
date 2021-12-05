import os
import pygame

class Cards:
    def __init__(self, img_path : str, name : str, size : tuple, position : tuple, index: tuple  = (0,0), outline : bool = False, selected : bool = False, clickable : bool = True) -> None:
        self._img_path = img_path
        self._name = name
        self._size = size
        self._position = position
        self._index = index
        self._outline = outline
        self._selected = selected
        self._clickable = clickable
    
    def draw_card(self, screen : pygame.Surface) -> None:
        card_image = pygame.image.load(self._img_path)
        card_resize = pygame.transform.scale(card_image,self._size)
        if self._selected == True and self._outline == True:
            pygame.draw.rect(screen, (0,0,255), pygame.Rect((self._position[0],self._position[1]), (100,100)), 15)
        screen.blit(card_resize,self._position)

    def point_in_rectanlge(self, px, py, rw, rh, rx, ry):
        if px > rx and px < rx  + rw:
            if py > ry and py < ry + rh:
                return True
        return False

    def clicked(self, pos : tuple)-> bool:
        if self.point_in_rectanlge(pos[0], pos[1], self._size[0], self._size[1], self._position[0], self._position[1]):
            self._selected = True
            return True
        self._selected = False
        return False

    @property
    def image(self):
        return self._img_path 

    @image.setter
    def image(self, img):
        self._img_path = os.path.join('assets','full-deck',f'{img}')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name
    
    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, idx):
        self._index = idx

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, pos):
        self._position = pos

    def get_info(self):
        return {
            "img_path" : self._img_path,
            "name" : self._name,
            "size" : self._size,
            "position" : self._position,
            "index" : self._index,
            "outline" : self._outline,
            "selected" : self._selected,
            "clickable" : self._clickable
        }

    @property
    def clickable(self, on=None):
        return self._clickable

    @clickable.setter
    def clickable(self,click):
        self._clickable = click

    def selected(self,selected):
        self._selected = selected
   
    






