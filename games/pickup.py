import os
import pygame

from cards import Cards

class card_game:

    def __init__(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = 725, 775
        self.green = 85,200,60
        self.screen = pygame.display.set_mode(self.size)

        self.cards = os.listdir(os.path.join("assets","full-deck"))
        self.initialized_cards = []
    
    def draw_cards(self) -> tuple:
        import random
        cards = []

        for deck in self.cards:
            turnover = random.randint(1,5)
            if turnover == 3 :
                card_path = os.path.join('assets','full-deck',f'{deck}')

                cards.append(Cards(card_path,deck,(100,100),(random.randint(0,self.width-100),random.randint(0,self.height-100))))
            else:
                card_path = os.path.join('assets','full-deck','cardback.PNG')

                cards.append(Cards(card_path,deck,(100,100),(random.randint(0,self.width-100),random.randint(0,self.height-100))))
        self.initialized_cards = cards       
        return cards

    def update_text(self, cards_left : int, start_time : float) -> None:
        font = pygame.font.Font(None, 54)
        black = 0,0,0

        passed_time = pygame.time.get_ticks() - start_time

        timer_text = font.render("Timer",True,black)
        timer = font.render(str(int(passed_time/1000)), True, black)

        cards_left_text = font.render("Cards Left",True,black)
        cards_count = font.render(str(cards_left), True, black)

        self.screen.blit(timer_text, (300, 25))
        self.screen.blit(timer, (300, 65))
        self.screen.blit(cards_left_text, (300, 110))
        self.screen.blit(cards_count, (300, 145))
        
    def check_complete(self, cards_left):
        if cards_left == 0:
            return True
        return False

    def answer_sound(self, answer: str) -> None:

        sound = pygame.mixer.Sound(os.path.join("assets","sounds",f"{answer}.mp3"))

        pygame.mixer.Sound.play(sound)
        pygame.mixer.music.stop()

    def play_game(self):
        import sys
        start_time = pygame.time.get_ticks()

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.screen.fill(self.green)
            if len(self.initialized_cards) == 0:
                create_cards = self.draw_cards()
            else:
                create_cards = self.initialized_cards

            self.update_text(len(self.cards),start_time)

            for card in create_cards:
                card.draw_card(self.screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                for card in create_cards:
                   if card.clicked(pos) and card.clickable:
                       print("removing")

                       self.cards.remove(card.name)
                       self.initialized_cards.remove(card)

            pygame.display.flip()

            if self.check_complete(len(self.cards)):
                self.screen.fill(self.green)
                create_cards = self.draw_cards()
                for card in create_cards:
                    card.draw_card(self.screen)
                    del card
                pygame.display.flip()
                self.answer_sound("winner")
                pygame.time.wait(6000)

                return
