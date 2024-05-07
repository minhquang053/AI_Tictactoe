from abc import ABC, abstractmethod
from mcts import MonteCarloTreeSearchNode
import numpy as np

class Player(ABC):
    def __init__(self, player_mask):
        self.player_mask = player_mask
    
    @abstractmethod
    def get_move(self, game_state):
        pass 

class HumanPlayer(Player):
    def get_move(self, game_state):
        pass

class AIPlayer(Player):
    def check_casual_move(self, board):
        return False, None

    def get_move(self, game_state):
        # Check for casual move first
        existed, move = self.check_casual_move(game_state.board)        
        if existed:
            return move

        # MCTS 
        root = MonteCarloTreeSearchNode(state=game_state, ai_mask=self.player_mask)
        selected_node = root.best_action()
        return selected_node.parent_action
