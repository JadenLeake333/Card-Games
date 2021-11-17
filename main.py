def draw_main_screen():
    import os
    from cards import Cards
    
    games = []
    directories = os.listdir("games")
    directories.pop() # Removes __pycache__
    y_multiple = 0
    for idx,mods in enumerate(directories):
        if idx != 0 and idx % 3 == 0:
            y_multiple += 250
            module = mods.replace(".py","")
            game_img = os.path.join('assets','thumbnails',f'{module}.PNG')
            games.append(Cards(game_img,f"{module}",(200,200),(520 / 9 + idx % 3 * 205, 720 / 40  + 1 * y_multiple), (0,0),f"{module}"))
        else:
            module = mods.replace(".py","")
            game_img = os.path.join('assets','thumbnails',f'{module}.PNG')
            games.append(Cards(game_img,f"{module}",(200,200),(520 / 9 + idx % 3 * 205, 720 / 40 + 1 * y_multiple), (0,0),f"{module}"))
    return games

def about_page():
    import pygame

def main():
    import os
    import pygame
    import importlib

    pygame.init()
    screen_size = height, width =  705, 725
    bg = (25, 25, 105)
    black = (0,0,0)
    button_size = 120,50
    screen = pygame.display.set_mode(screen_size)

    game_list = draw_main_screen()

    font = pygame.font.Font(None, 42)

    while True:
        screen.fill(bg)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        for game in game_list:
            game.draw_card(screen)
            text_postition = game.get_position()
            game_name = font.render(f"{game.get_name()}",True,black)
            screen.blit(game_name, (text_postition[0], text_postition[1] + 200))

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for game in game_list:
                if game.clicked(pos):
                    play = importlib.import_module(f"games.{game.get_name()}")
                    game_selection = play.card_game()
                    game_selection.play_game()

        pygame.display.flip()

    pygame.quit()
    sys.exit
    
if __name__ == '__main__':
    main()