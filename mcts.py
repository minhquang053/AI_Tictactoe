import numpy as np
import time
import math
from collections import defaultdict

class MonteCarloTreeSearchNode():
    def __init__(self, state, ai_mask, parent=None, parent_action=None):
        self.state = state
        self.ai_mask = ai_mask
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        self._untried_actions = self.state.get_near_center_legal_actions()
        return self._untried_actions
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses
    
    def n(self):
        return self._number_of_visits
    
    def expand(self):
        action = self._untried_actions.pop(0)
        next_state = self.state.simulate_move(action)
        child_node = MonteCarloTreeSearchNode(next_state, self.ai_mask, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.check_game_over()[0]

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.check_game_over()[0]:
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.simulate_move(action)
                 
        return current_rollout_state.game_result(self.ai_mask)

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1 
        if self.parent:
            self.parent.backpropagate(result)
    
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    
    def best_child(self, c_param=0.1):
        choice_weights = [(c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choice_weights)]
    
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self, iteration=10000, timeout=8):
        num_simulation = iteration
    
        start = time.time()
        while time.time() - start < timeout and num_simulation > 0: 
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
            num_simulation -= 1

        print(f"num simulation: {iteration - num_simulation},", end=" ")
        return self.best_child(c_param=math.sqrt(2))
