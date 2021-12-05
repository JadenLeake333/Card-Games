import os
import random
import pygame
# TO DO
# Not indexing properly
from cards import Cards

class card_game:

    def __init__(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = 725, 775
        self.green = 85,200,60
        self.screen = pygame.display.set_mode(self.size)
        self.board = [
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
        self.cover = None

        self.cards = os.listdir(os.path.join("assets","full-deck"))
        self.cards.remove("cardback.PNG")
        random.shuffle(self.cards)
        self.deck = []
    
    def fill_board(self):
        for idx,i in enumerate(self.board):
            for jdx,j in enumerate(self.board[idx]):
                if self.board[idx][jdx] == 0:
                    choice = random.choice(self.cards)
                    self.board[idx][jdx] = choice
                    self.cards.remove(choice)
        print(self.board)
           
    def draw_cards(self) -> tuple:
        import random
        cards = []

        for idx,i in enumerate(self.board):
            for jdx,j in enumerate(self.board[idx]):
                card_x = 520 / 9 + jdx * 140
                card_y = 720 / 2 + idx * 105

                card_path = os.path.join('assets','full-deck','cardback.PNG')

                cards.append(Cards(card_path,self.board[idx][jdx],(100,100),(card_x, card_y),(idx,jdx), outline = False, clickable = False))
            
        if len(self.deck) == 0:
            for deck in self.cards:
                card_name = deck.split("_")[0]
                card_path = os.path.join('assets','full-deck','cardback.PNG')

                if card_name in ["jack", "queen", "king"]:
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(5,5), clickable=True))
                    continue
                if card_name == 'ace':
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(0,0), clickable=True))
                    continue
                if int(card_name) == 10: # Special case at the end of a the second row
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(1,4), clickable=True))
                    continue
                if int(card_name) <= 5:
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(0,int(card_name) - 1), clickable=True))
                    continue
                if int(card_name) > 5:
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(1,int(card_name) % 5 - 1), clickable=True))
                    continue
        self.cover = cards
        return cards

    def check_complete(self):
        if len(self.cover) == 1:
            return True
        return False

    def index_card(self, card):
    # Set index of card based on its number
        card_name = card.name.split("_")[0]

        if card_name in ["jack", "queen", "king"]:
            card.index = (5,5)
            card.position = (420, 200)
        elif card_name == 'ace':
            card.index = (0,0)
        elif int(card_name) == 10: # Special case at the end of a the second row
            card.index = (1,4)
        elif int(card_name) <= 5:
            card.index = (0,int(card_name) - 1)
        elif int(card_name) > 5:
            card.index = (1,int(card_name) % 5 - 1)
        


    def answer_sound(self, answer: str) -> None:

        sound = pygame.mixer.Sound(os.path.join("assets","sounds",f"{answer}.mp3"))

        pygame.mixer.Sound.play(sound)
        pygame.mixer.music.stop()

    def check_deck(self, card_index):
        i,j = card_index
        for cards in self.cover:
            if cards.name == self.board[i][j]:
                cards.image = cards.name
                cards.clickable = True
                cards.position = (520,200)
                cards.draw_card(self.screen)
                return

    def check_index(self, card):
        indexs = card.index
        card_x = 520 / 9 + indexs[1] * 140
        card_y = 720 / 2 + indexs[0] * 105
        if indexs != (5,5):
            card.position = (card_x, card_y)
            return True
        return False

    def play_game(self):
        import os
        import sys

        start_time = pygame.time.get_ticks()

        self.fill_board()

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.screen.fill(self.green)

            if not self.cover:
                create_cards = self.draw_cards()
                for card in create_cards:
                    card.draw_card(self.screen)
            else:
                for card in self.cover:
                    card.draw_card(self.screen)

            for card in self.deck:
                card.draw_card(self.screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                cards = self.deck + self.cover
                for card in cards:
                    if card.clicked(pos) and card.clickable:
                        card.image = card.name
                        card.position = (420,200)
                        if self.check_index(card):
                            card.clickable = False
                            self.check_deck(card.index)
                            self.index_card(card)
                            if card in self.cover:
                                self.cover.remove(card)
                                if card not in self.deck:
                                    self.deck.append(card)
                        break

            pygame.display.flip()

            if self.check_complete():
                self.screen.fill(self.green)
                create_cards = self.draw_cards()
                for card in create_cards:
                    card.draw_card(self.screen)
                    del card
                pygame.display.flip()
                self.answer_sound("winner")
                pygame.time.wait(6000)

                return
