def main():
    pygame.init()
    clock = pygame.time.Clock()
    size = [200, 200]
    bg = [255, 255, 255]

    screen = pygame.display.set_mode(size)

    button = pygame.Rect(100, 100, 50, 50)  # creates a rect object

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button.collidepoint(mouse_pos):
                    # prints current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))

        screen.fill(bg)

        pygame.draw.rect(screen, [255, 0, 0], button)  # draw button

        pygame.display.update()

    pygame.quit()
    sys.exit
if __name__ == '__main__':
    import pygame
    from memorize import card_game
    game = card_game()
    game.play_game()
    # main()