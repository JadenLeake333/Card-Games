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

        self.cards = {
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
            9 : 0,
            10 : 0,
            "J" : 0,
            "Q" : 0,
            "K" : 0,
            "A" : 0
        }

        self.game_board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0],
        ]

    def print_board(self, board : list) -> None:
        for i in board:
            for j in i:
                print(j,end=" ")
            print("\n")

    def fill_board(self):
        import random

        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                if self.game_board[i][j] == 0:
                    get_card_index = random.choice(list(self.cards.keys()))
                    
                    self.game_board[i][j] = get_card_index
                    self.cards[get_card_index] = self.cards[get_card_index] + 1

                    if self.cards[get_card_index] == 2:
                        self.cards.pop(get_card_index)

        return self.game_board

    def reset_game():
        pass 

    def check_complete(self, board : list) -> None:
        for i in board:
            for j in i:
                if j == 0:
                    return False
        return True

    def draw_cards(self, board : list, cover : list) -> tuple:
        cards = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                card_x = 520 / 9 + j * 120
                card_y = 720 / 40 + i * 105
                if cover[i][j] == 0:
                    card_path = os.path.join('assets','memorize-cards','cardback.PNG')

                    cards.append(Cards(card_path,board[i][j],(100,100),(card_x,card_y),(i,j)))
                else:
                    card_path = os.path.join('assets','memorize-cards',f'{board[i][j]}-card.PNG')

                    cards.append(Cards(card_path,board[i][j],(100,100),(card_x,card_y),(i,j)))
                
        return cards

    def check_card(self, coords : dict, cover : list, board : list, x: int, y : int):
        clicked = None
        for idx in coords:
            i,j = idx.split(",")
            i,j = int(i),int(j)
            if cover[i][j] == 0:
                if x > int(coords[idx][0]) and x < int(coords[idx][0]) + (j+1)*75 and y > int(coords[idx][1]) and y < int(coords[idx][1]) + (i+1)*100:
                    clicked = i,j
        return clicked

    def answer_sound(self, answer: str) -> None:

        sound = pygame.mixer.Sound(os.path.join("assets","sounds",f"{answer}.mp3"))

        pygame.mixer.Sound.play(sound)
        pygame.mixer.music.stop()

    def update_text(self, misses : int, start_time : float) -> None:
        font = pygame.font.Font(None, 54)
        black = 0,0,0

        passed_time = pygame.time.get_ticks() - start_time

        timer_text = font.render("Timer",True,black)
        timer = font.render(str(int(passed_time/1000)), True, black)

        miss_text = font.render("Misses",True,black)
        miss = font.render(str(misses), True, black)

        self.screen.blit(timer_text, (575, 25))
        self.screen.blit(timer, (575, 65))
        self.screen.blit(miss_text, (575, 110))
        self.screen.blit(miss, (575, 145))

    def play_game(self):
        import sys

        board = self.fill_board()

        self.print_board(board)

        game_cover = [
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0],
            ]

        guesses = []
        misses = 0

        start_time = pygame.time.get_ticks()

        game_over = False
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.screen.fill(self.green)
            create_cards = self.draw_cards(board, game_cover)
            
            if self.check_complete(game_cover):
                if misses == 0:
                    self.answer_sound("perfect")
                self.answer_sound("winner")
                pygame.time.wait(6000)
                game_over = True

            for card in create_cards:
                card.draw_card(self.screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                for card in create_cards:
                   if card.clicked(pos):
                       i,j = card.get_index()
                       if game_cover[i][j] == 0:
                        game_cover[i][j] = board[i][j]
                        guesses.append((i,j,board[i][j]))

                # Redraw in case guess is incorrect
                redraw_cards = self.draw_cards(board, game_cover)
                for card in redraw_cards:
                    card.draw_card(self.screen)

                pygame.display.flip()

                if len(guesses) == 2:

                    if guesses[0][2] == guesses[1][2]:
                        # play sound
                        self.answer_sound("correct")
                        guesses.clear()
                    else:
                        # Reset clicked numbers
                        self.answer_sound("incorrect")
                        pygame.time.wait(1000)
                        game_cover[guesses[0][0]][guesses[0][1]], game_cover[guesses[1][0]][guesses[1][1]] = 0, 0
                        misses += 1
                        guesses.clear()

            self.update_text(misses, start_time)
            # Display on screen
            pygame.display.flip()

