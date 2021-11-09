
class card_game:
    def __init__(self):
        self.cards = cards = {
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

    def print_board(self, board):
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

    def check_complete(self, board):
        for i in board:
            for j in i:
                if j == 0:
                    return False
        return True

if __name__ == "__main__":
    import os

    game = card_game()
    stop_playing = False

    game_board = game.fill_board()
    game.print_board(game_board)
    
    while not stop_playing:
    
        coord1 = input("Name a cell: ").split(",")
        temp = game_cover

        game_cover[int(coord1[0])][int(coord1[1])] = game_board[int(coord1[0])][int(coord1[1])]

        game.print_board(game_cover)

        coord2 = input("Name a cell: ").split(",")

        if game_board[int(coord1[0])][int(coord1[1])] == game_board[int(coord2[0])][int(coord2[1])]:

            game_cover[int(coord2[0])][int(coord2[1])] = game_board[int(coord2[0])][int(coord2[1])]

            game.print_board(game_cover)

            if game.check_complete(game_cover):
                stop_playing = True
            continue
        else:

            game_cover[int(coord1[0])][int(coord1[1])] = 0

            game_cover[int(coord2[0])][int(coord2[1])] = 0

            game.print_board(game_cover)

