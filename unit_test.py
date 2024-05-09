from tictactoe import TicTacToe

def test_move():
    test = TicTacToe(10, 5)
    test.move((6, 1))
    test.move((7, 1))
    test.move((6, 2))
    test.move((7, 2))
    test.move((6, 3))
    test.move((7, 3))
    test.move((1, 1))
    test.move((7, 4))
    test.move((6, 4))
    test.print_board()

    print(test.get_casual_move())
    
if __name__ == "__main__":
    test_move()
