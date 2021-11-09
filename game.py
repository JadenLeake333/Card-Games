import os
import pygame

def draw_cards(screen : int, board : list):
    coords = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                card = pygame.image.load(os.path.join('assets','cardback.PNG'))
                resize_card = pygame.transform.scale(card,(100, 100))
                screen.blit(resize_card, (520 / 9 + j * 75, 720 / 40 + i * 100))
                coords.update({f'{i},{j}' : [520 / 9 + j * 75 , 720 / 40 + i * 100]})
            else:
                card = pygame.image.load(os.path.join('assets',f'{board[i][j]}-card.PNG'))
                resize_card = pygame.transform.scale(card,(100, 100))
                screen.blit(resize_card, (520 / 9 + j * 75, 720 / 40 + i * 100))
                coords.update({f'{i},{j}' : [520 / 9 + j * 75 , 720 / 40 + i * 100]})
            
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

def answer_sound(answer: bool) -> None:

    correct = pygame.mixer.Sound(os.path.join("assets","sounds","correct.mp3"))
    incorrect = pygame.mixer.Sound(os.path.join("assets","sounds","incorrect.mp3"))

    if answer:
        pygame.mixer.Sound.play(correct)
        pygame.mixer.music.stop()
    else:
        pygame.mixer.Sound.play(incorrect)
        pygame.mixer.music.stop()

def main():
    import sys
    from memorize import card_game

    pygame.init()

    clock = pygame.time.Clock()
    game = card_game()
    board = game.fill_board()

    game.print_board(board)

    size = width, height = 620, 720
    font = pygame.font.Font(None, 54)
    green = 85,200,60
    black = 0,0,0

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

    while 1:

        passed_time = pygame.time.get_ticks() - start_time

        timer_text = font.render("Timer",True,black)
        timer = font.render(str(int(passed_time/1000)), True, black)

        miss_text = font.render("Misses",True,black)
        miss = font.render(str(misses), True, black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        screen.fill(green)
        coords = draw_cards(screen, game_cover)
        screen.blit(timer_text, (460, 220))
        screen.blit(timer, (460, 260))
        screen.blit(miss_text, (460, 320))
        screen.blit(miss, (460, 360))


        if game.check_complete(game_cover):
            for i in range(100):
                answer_sound(True)


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

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
                    answer_sound(True)
                    guesses.clear()
                else:
                    # Reset clicked numbers
                    answer_sound(False)
                    pygame.time.wait(1000)
                    game_cover[guesses[0][0]][guesses[0][1]], game_cover[guesses[1][0]][guesses[1][1]] = 0, 0
                    misses += 1
                    guesses.clear()

        # Display on screen
        pygame.display.flip()

main()