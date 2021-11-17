import os
import pygame

class Cards:
    def __init__(self, img_path : str, name : str, size : tuple, position : tuple, index: tuple  = (0,0), outline : bool = False, selected : bool = False, clickable : bool = True) -> None:
        self.img_path = img_path
        self.name = name
        self.size = size
        self.position = position
        self.index = index
        self.outline = outline
        self.selected = selected
        self.clickable = clickable
    
    def draw_card(self, screen : pygame.Surface) -> None:
        card_image = pygame.image.load(self.img_path)
        card_resize = pygame.transform.scale(card_image,self.size)
        if self.selected == True and self.outline == True:
            pygame.draw.rect(screen, (0,0,255), pygame.Rect((self.position[0],self.position[1]), (100,100)), 15)
        screen.blit(card_resize,self.position)

    def point_in_rectanlge(self, px, py, rw, rh, rx, ry):
        if px > rx and px < rx  + rw:
            if py > ry and py < ry + rh:
                return True
        return False

    def clicked(self, pos : tuple)-> bool:
        if self.point_in_rectanlge(pos[0], pos[1], self.size[0], self.size[1], self.position[0], self.position[1]):
            self.selected = True
            return True
        self.selected = False
        return False

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index

    def get_position(self):
        return self.position
    
    def set_position(self, pos):
        self.position = pos
        self.selected = False
    
    def set_image(self, img):
        self.img_path = os.path.join('assets','full-deck',f'{img}')

    def is_clickable(self):
        return self.clickable



