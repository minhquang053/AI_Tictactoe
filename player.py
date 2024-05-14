from abc import ABC, abstractmethod
from mcts import MonteCarloTreeSearchNode
import pygame
import sys
import time

class Player(ABC):
    def __init__(self, player_mask):
        self.player_mask = player_mask
    
    @abstractmethod
    def get_move(self, game_state):
        pass 

class HumanPlayer(Player):
    def __init__(self, player_mask, screen_size=400):
        super().__init__(player_mask)
        self.screen_size = screen_size

    def get_move(self, game_state, move_timeout=-1):
        # won't be needed
        move_timeout

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and game_state.current_turn == self.player_mask:
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // (self.screen_size // game_state._n)
                    col = mouse_pos[0] // (self.screen_size // game_state._n)
                    if 0 <= row < game_state._n and 0 <= col < game_state._n and game_state.board[row][col] == 0:
                        return (row, col)  # Return the selected move

class AIPlayer(Player):
    def visual_test(self, game_state, num_sim):
        root = MonteCarloTreeSearchNode(state=game_state, ai_mask=self.player_mask)
        selected_node = root.best_action(iteration=num_sim, timeout=100)
        return root, selected_node.parent_action

    def get_move(self, game_state, move_timeout):
        # Check for casual move first
        start = time.time()
        move = game_state.get_casual_move()   
        if move:
            while (time.time() - start) + 0.01 < move_timeout:
                pass
            return move

        time_left = move_timeout - (time.time() - start) - 0.01
        
        # MCTS 
        root = MonteCarloTreeSearchNode(state=game_state, ai_mask=self.player_mask)
        selected_node = root.best_action(timeout=time_left)
        print(f"time taken: {time.time() - start}s")
        return selected_node.parent_action
