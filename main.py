from tictactoe import TicTacToe
from player import AIPlayer

def main():
    game = TicTacToe(n=3, winning_condition=3)
    player_1 = AIPlayer(1)
    player_2 = AIPlayer(-1)

    while not game.check_game_over()[0]: 
        # check player turn
        if game.current_turn == 1:
            player = player_1 
        else:
            player = player_2
        
        action = player.get_move(game)
        game.move(action)
        game.print_board()

    winner = game.check_game_over()[1]
    if winner > 0:
        print("Player 1 won")
    elif winner < 0:
        print("Player 2 won")
    else:
        print("Tie")

if __name__ == "__main__":
    main()
