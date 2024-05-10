from tictactoe import TicTacToe
from player import AIPlayer
import networkx as nx
import matplotlib.pyplot as plt

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

def visualize_tree(num_simulation):
    game = TicTacToe(n=10, winning_condition=5)
    ai = AIPlayer(-1)
    root_node, action = ai.visual_test(game, num_simulation)
    print(action)

    G = nx.DiGraph()
    node_queue = [root_node]
    node_id_map = {root_node: 0}  # Map nodes to unique IDs for plotting

    while node_queue:
        current_node = node_queue.pop(0)
        current_node_id = node_id_map[current_node]

        # Add current node to the graph
        G.add_node(current_node_id, label=f"Visits: {current_node._number_of_visits}")

        if current_node.parent:
            parent_id = node_id_map[current_node.parent]
            G.add_edge(parent_id, current_node_id, label=str(current_node.parent_action))

        for child in current_node.children:
            child_id = len(node_id_map)  # New ID for each child node
            node_id_map[child] = child_id
            node_queue.append(child)

    # Plot the tree graph
    pos = nx.spring_layout(G)  # Layout the nodes using the spring layout algorithm
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, font_color="black")
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Monte Carlo Tree Search Tree Visualization")
    plt.show()
    
if __name__ == "__main__":
    # test_move()
    visualize_tree(50)
