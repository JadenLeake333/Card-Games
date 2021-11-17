import os
import random
import pygame

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
        self.cover = [
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]

        self.cards = os.listdir(os.path.join("assets","full-deck"))
        self.cards.remove("cardback.PNG")
        random.shuffle(self.cards)
        self.deck = []
    
    def fill_board(self):

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    choice = random.choice(self.cards)
                    self.board[i][j] = choice
                    self.cards.remove(choice)
                    
    def draw_cards(self) -> tuple:
        import random
        cards = []

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                card_x = 520 / 9 + j * 140
                card_y = 720 / 2 + i * 105

                card_path = os.path.join('assets','full-deck','cardback.PNG')

                cards.append(Cards(card_path,self.board[i][j],(100,100),(card_x, card_y),(i,j), outline = True, clickable = False))
            
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
                if int(card_name) == 10:
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(1,4), clickable=True))
                    continue
                if int(card_name) <= 5:
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(0,int(card_name) - 1), clickable=True))
                    continue
                if int(card_name) > 5:
                    self.deck.append(Cards(card_path,deck,(100,100),(300, 200),(1,int(card_name) % 5 - 1), clickable=True))
                    continue

        return cards

    def check_complete(self, cards_left):
        if cards_left == 0:
            return True
        return False

    def answer_sound(self, answer: str) -> None:

        sound = pygame.mixer.Sound(os.path.join("assets","sounds",f"{answer}.mp3"))

        pygame.mixer.Sound.play(sound)
        pygame.mixer.music.stop()

    def check_index(self, card_one, card_two_idx):
        card_one_idx = card_one.get_index()
        card_x = 520 / 9 + card_two_idx[1] * 140
        card_y = 720 / 2 + card_two_idx[0] * 105
        if card_one_idx == (5,5):
            return False
        elif card_one_idx == card_two_idx:
            card_one.set_position((card_x, card_y))

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

            create_cards = self.draw_cards()

            for card in create_cards:
                card.draw_card(self.screen)
            
            for card in self.deck:
                card.draw_card(self.screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                for card in self.deck:
                    if card.clicked(pos) and card.is_clickable():

                        card.set_image(card.get_name())
                        card.set_position((420,200))
                        i,j = card.get_index()
                        self.check_index(card,(i,j))
                        card.draw_card(self.screen)
                        #self.cards.remove(card.get_name())
                        #del card
                        break

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
