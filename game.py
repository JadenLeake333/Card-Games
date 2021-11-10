import os
import pygame

def draw_cards(screen : pygame.Surface, board : list) -> tuple:
    coords = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            card_x = 520 / 9 + j * 125
            card_y = 720 / 40 + i * 110
            if board[i][j] == 0:
                card = pygame.image.load(os.path.join('assets','cards','cardback.PNG'))
                resize_card = pygame.transform.scale(card,(100, 100))
                screen.blit(resize_card, (card_x, card_y))
                coords.update({f'{i},{j}' : [card_x , card_y]})
            else:
                card = pygame.image.load(os.path.join('assets','cards',f'{board[i][j]}-card.PNG'))
                resize_card = pygame.transform.scale(card,(100, 100))
                screen.blit(resize_card, (card_x, card_y))
                coords.update({f'{i},{j}' : [card_x , card_y]})
            
    return coords

def check_card(coords : dict, cover : list, board : list, x: int, y : int):
    clicked = None
    for idx in coords:
        i,j = idx.split(",")
        i,j = int(i),int(j)
        if cover[i][j] == 0:
            if x > int(coords[idx][0]) and x < int(coords[idx][0]) + (j+1)*75 and y > int(coords[idx][1]) and y < int(coords[idx][1]) + (i+1)*100:
                clicked = i,j
    return clicked

def answer_sound(answer: str) -> None:

    sound = pygame.mixer.Sound(os.path.join("assets","sounds",f"{answer}.mp3"))

    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

def update_text(misses : int, start_time : float, screen : pygame.Surface) -> None:
    font = pygame.font.Font(None, 54)
    black = 0,0,0

    passed_time = pygame.time.get_ticks() - start_time

    timer_text = font.render("Timer",True,black)
    timer = font.render(str(int(passed_time/1000)), True, black)

    miss_text = font.render("Misses",True,black)
    miss = font.render(str(misses), True, black)

    screen.blit(timer_text, (575, 25))
    screen.blit(timer, (575, 65))
    screen.blit(miss_text, (575, 110))
    screen.blit(miss, (575, 145))

def play_game():
    import sys
    from memorize import card_game

    pygame.init()

    clock = pygame.time.Clock()
    game = card_game()
    board = game.fill_board()

    game.print_board(board)

    size = width, height = 725, 775
    green = 85,200,60

    screen = pygame.display.set_mode(size)

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
        
        screen.fill(green)
        coords = draw_cards(screen, game_cover)
        
        if game.check_complete(game_cover):
            if misses == 0:
                answer_sound("perfect")
            answer_sound("winner")
            pygame.time.wait(6000)
            game_over = True


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
            clicked_card = check_card(coords,game_cover, board,*pos)

            if clicked_card == None:
                continue

            game_cover[clicked_card[0]][clicked_card[1]] = board[clicked_card[0]][clicked_card[1]]

            guesses.append((clicked_card[0],clicked_card[1],board[clicked_card[0]][clicked_card[1]]))

            # Redraw in case guess is incorrect
            draw_cards(screen, game_cover)
            pygame.display.flip()

            if len(guesses) == 2:

                if guesses[0][2] == guesses[1][2]:
                    # play sound
                    answer_sound("correct")
                    guesses.clear()
                else:
                    # Reset clicked numbers
                    answer_sound("incorrect")
                    pygame.time.wait(1000)
                    game_cover[guesses[0][0]][guesses[0][1]], game_cover[guesses[1][0]][guesses[1][1]] = 0, 0
                    misses += 1
                    guesses.clear()

        update_text(misses, start_time, screen)
        # Display on screen
        pygame.display.flip()