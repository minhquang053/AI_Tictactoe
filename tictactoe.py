import copy
import numpy as np

class TicTacToe:
    def __init__(self, n, winning_condition):
        if n < winning_condition:
            raise Exception("Invalid setting")

        # Inital state of the tictactoe game
        self._n = n
        self.board = [[0 for i in range(n)] for j in range(n)]
        self.win_cond = winning_condition
        self.current_turn = 1
    
    def print_board(self):
        print(f"Player {-self.current_turn} turn")
        for i in range(self._n):
            # Print the row with elements separated by vertical bars
            row_str = " | ".join(str(self.board[i][j]) for j in range(self._n))
            print(row_str)
            
            # Print a horizontal line between rows (except after the last row)
            if i < self._n - 1:
                print("-" * len(row_str))

    def get_legal_actions(self):
        np_board = np.array(self.board)
        zero_indices = np.where(np_board == 0)
        available_positions = list(zip(zero_indices[0], zero_indices[1]))

        # Calculate center position
        center_row = self._n // 2  # Assuming self._n is the row length (equal to col length)
        center_col = self._n // 2
        
        # Sort positions based on distance from the center
        def distance_from_center(pos):
            row, col = pos
            return abs(row - center_row) + abs(col - center_col)  # Manhattan distance

        available_positions.sort(key=distance_from_center)

        return available_positions

    def is_potential_segment(self, segment, player):
        """ Check if a segment of marks has (n-2) consecutive marks of the same player with open ends """
        mid = len(segment) // 2

        # if opponent already played here, the segment absolutely gets useless
        if segment.count(-player) > 0:
            return False, None
        
        if segment.count(player) == self.win_cond - 2 and segment[mid-1] == player and segment[mid+1] == player:
            return True, [i for i, x in enumerate(segment) if x == 0]
        return False, None
    
    def get_casual_move(self):
        # casual move that player should do when in certain states
        available_moves = self.get_legal_actions()
        board_1 = copy.deepcopy(self.board)
        board_2 = copy.deepcopy(self.board) 

        for move in available_moves:
            # check for move to win immediately
            board_1[move[0]][move[1]] = self.current_turn 
            board_2[move[0]][move[1]] = -self.current_turn

            for i in range(self._n):
                for j in range(self._n - (self.win_cond - 1)):
                    if all(board_1[i][j + k] == self.current_turn for k in range(self.win_cond)):
                        return move

            for i in range(self._n - (self.win_cond - 1)):
                for j in range(self._n):
                    if all(board_1[i + k][j] == self.current_turn for k in range(self.win_cond)):
                        return move

            for i in range(self._n - (self.win_cond - 1)):
                for j in range(self._n - (self.win_cond - 1)):
                    if all(board_1[i + k][j + k] == self.current_turn for k in range(self.win_cond)):
                        return move

            for i in range(self._n - (self.win_cond - 1)):
                for j in range((self.win_cond - 1), self._n):
                    if all(board_1[i + k][j - k] == self.current_turn for k in range(self.win_cond)):
                        return move 
                    
            # check for move to stop opponent from winning next turn
            for i in range(self._n):
                for j in range(self._n - (self.win_cond - 1)):
                    if all(board_2[i][j + k] == -self.current_turn for k in range(self.win_cond)):
                        return move

            for i in range(self._n - (self.win_cond - 1)):
                for j in range(self._n):
                    if all(board_2[i + k][j] == -self.current_turn for k in range(self.win_cond)):
                        return move

            for i in range(self._n - (self.win_cond - 1)):
                for j in range(self._n - (self.win_cond - 1)):
                    if all(board_2[i + k][j + k] == -self.current_turn for k in range(self.win_cond)):
                        return move

            for i in range(self._n - (self.win_cond - 1)):
                for j in range((self.win_cond - 1), self._n):
                    if all(board_2[i + k][j - k] == -self.current_turn for k in range(self.win_cond)):
                        return move 
             
            # Reset board
            board_1[move[0]][move[1]] = 0
            board_2[move[0]][move[1]] = 0
        
        if self._n > self.win_cond:
            # check for moves that leads current player to potential winning
            # or stop opponent to play moves leading to potential winning
            potential_wins = []
            potential_loses = []
            for i in range(self._n):
                for j in range(self._n - (self.win_cond - 1)):
                    row_segment = [self.board[i][j + k] for k in range(self.win_cond)]
                    is_potential, positions = self.is_potential_segment(row_segment, self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_wins.append((i, j + pos))
                    is_potential, positions = self.is_potential_segment(row_segment, -self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_loses.append((i, j + pos))

            for i in range(self._n - (self.win_cond - 1)):
                for j in range(self._n):
                    col_segment = [self.board[i + k][j] for k in range(self.win_cond)]
                    is_potential, positions = self.is_potential_segment(col_segment, self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_wins.append((i + pos, j))
                    is_potential, positions = self.is_potential_segment(col_segment, -self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_loses.append((i + pos, j))

            for i in range(self._n - (self.win_cond - 1)):
                for j in range(self._n - (self.win_cond - 1)):
                    diag_segment = [self.board[i + k][j + k] for k in range(self.win_cond)]
                    is_potential, positions = self.is_potential_segment(diag_segment, self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_wins.append((i + pos, j + pos))
                    is_potential, positions = self.is_potential_segment(diag_segment, -self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_loses.append((i + pos, j + pos))

            for i in range(self._n - (self.win_cond - 1)):
                for j in range((self.win_cond - 1), self._n):
                    diag_segment = [self.board[i + k][j - k] for k in range(self.win_cond)]
                    is_potential, positions = self.is_potential_segment(diag_segment, self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_wins.append((i + pos, j - pos))
                    is_potential, positions = self.is_potential_segment(diag_segment, -self.current_turn)
                    if is_potential:
                        for pos in positions:
                            potential_loses.append((i + pos, j - pos))
            
            dup = set(potential_wins).intersection((potential_loses))
            if len(dup) > 0:
                print("HERE_3.1:", end=" ")
                print(dup)
                return next(iter(dup))
            if len(potential_wins) > 0:
                print("HERE_3.2:", end=" ")
                print(potential_wins)
                return potential_wins[0]
            if len(potential_loses) > 0:
                print("HERE_3.3:", end=" ")
                print(potential_loses)
                return potential_loses[0]

        return None

    def check_game_over(self):
        # Check rows for a win 
        for i in range(self._n):
            for j in range(self._n - (self.win_cond - 1)):
                if all(self.board[i][j + k] == -self.current_turn for k in range(self.win_cond)):
                    return True, -self.current_turn

        # Check columns for a win
        for i in range(self._n - (self.win_cond - 1)):
            for j in range(self._n):
                if all(self.board[i + k][j] == -self.current_turn for k in range(self.win_cond)):
                    return True, -self.current_turn

        # Check diagonals (top-left to bottom-right) for a win
        for i in range(self._n - (self.win_cond - 1)):
            for j in range(self._n - (self.win_cond - 1)):
                if all(self.board[i + k][j + k] == -self.current_turn for k in range(self.win_cond)):
                    return True, -self.current_turn

        # Check diagonals (top-right to bottom-left) for a win
        for i in range(self._n - (self.win_cond - 1)):
            for j in range((self.win_cond - 1), self._n):
                if all(self.board[i + k][j - k] == -self.current_turn for k in range(self.win_cond)):
                    return True, -self.current_turn

        if len(self.get_legal_actions()) == 0:
            return True, 0

        return False, None
    
    def game_result(self, ai_mask):
        is_over, winner = self.check_game_over()
        if not is_over:
            raise Exception("The game hasn't ended yet")

        if ai_mask == winner:
            return 1
        elif ai_mask == -winner:
            return -1 
        else:
            return 0

    def move(self, action):
        self.board[action[0]][action[1]] = self.current_turn
        self.current_turn = -self.current_turn
        
    def simulate_move(self, action):
        new_state = copy.deepcopy(self)
        new_state.board[action[0]][action[1]] = self.current_turn
        new_state.current_turn = -self.current_turn
        return new_state
