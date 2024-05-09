import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame_menu
import sys
from tictactoe import TicTacToe
from player import AIPlayer, HumanPlayer

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
N = 10
MOVE_TIMEOUT = 2
SQUARE_SIZE = SCREEN_WIDTH // N
LINE_WIDTH = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

PLAYER_1 = "Human"
PLAYER_2 = "AI"

def change_player(value, player_type):
    global PLAYER_1, PLAYER_2
    selected, _ = value
    if "1" in player_type:
        PLAYER_1 = selected[0]
    elif "2" in player_type:
        PLAYER_2 = selected[0]

def draw_board(screen, game):
    # Draw the grid lines
    for i in range(1, N):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SCREEN_HEIGHT), 3)
    for i in range(1, N):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (SCREEN_WIDTH, i * SQUARE_SIZE), 3)

    # Draw X's and O's
    for row in range(N):
        for col in range(N):
            mark = game.board[row][col]
            if mark == 1:  # X
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE), LINE_WIDTH)
            elif mark == -1:  # O
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - LINE_WIDTH + 1, LINE_WIDTH)
                
def start_game(screen):
    def game_loop(screen):
        restart = True
        while restart:
            game = TicTacToe(n=N, winning_condition=5)
            player_1 = HumanPlayer(1) if PLAYER_1 == "Human" else AIPlayer(1)
            player_2 = HumanPlayer(-1) if PLAYER_2 == "Human" else AIPlayer(-1)
            screen.fill(WHITE)
            draw_board(screen, game)
            pygame.display.flip()

            clock = pygame.time.Clock()
            running = True
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
                if not game.check_game_over()[0]:
                    if game.current_turn == player_1.player_mask:
                        action = player_1.get_move(game, MOVE_TIMEOUT)
                    else:
                        action = player_2.get_move(game, MOVE_TIMEOUT)
                    
                    game.move(action)
                        
                    screen.fill(WHITE)
                    draw_board(screen, game)
                    pygame.display.flip()
                    clock.tick(30)
                else:
                    winner_mask = game.check_game_over()[1]
                    if winner_mask > 0:
                        winner = "Player 1"
                    elif winner_mask < 0:
                        winner = "Player 2"
                    else:
                        winner = "Tie"

                    restart = show_game_over_dialog(screen, winner)
                    break
    
    return game_loop

def show_game_over_dialog(screen, winner):
    global PLAYER_1, PLAYER_2
    font = pygame.font.Font(None, 36)
    if winner == "Tie":
        text_surface = font.render(f"Tie", True, BLACK)
    else:
        text_surface = font.render(f"{winner} wins!", True, BLACK)

    # Create a background rectangle
    background_rect = pygame.Rect(50, 10, SCREEN_WIDTH - 100, 40)
    pygame.draw.rect(screen, WHITE, background_rect)  # Draw a white background behind the text
    pygame.draw.rect(screen, GREY, background_rect, 3)  # Draw a black border
    screen.blit(text_surface, (120, 18))  # Draw the text with an offset for positioning

    # Display options
    font = pygame.font.Font(None, 24)
    continue_text = font.render("Continue", True, BLACK)
    main_menu_text = font.render("Go to main menu", True, BLACK)

    continue_button = pygame.Rect(50, 340, 100, 50)
    main_menu_button = pygame.Rect(200, 340, 150, 50)

    pygame.draw.rect(screen, GREEN, continue_button)
    pygame.draw.rect(screen, GREY, continue_button, 3)  # Draw a black border
    pygame.draw.rect(screen, RED, main_menu_button)
    pygame.draw.rect(screen, GREY, main_menu_button, 3)  # Draw a black border
    
    # Position the text within the buttons
    continue_text_rect = continue_text.get_rect(center=continue_button.center)
    main_menu_text_rect = main_menu_text.get_rect(center=main_menu_button.center)

    screen.blit(continue_text, continue_text_rect)
    screen.blit(main_menu_text, main_menu_text_rect)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if continue_button.collidepoint(mouse_pos):
                    return True
                elif main_menu_button.collidepoint(mouse_pos):
                    PLAYER_1 = "Human"
                    PLAYER_2 = "AI"
                    return False  # Return to main menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")

    menu = pygame_menu.Menu("Tic Tac Toe", SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)

     # Add player type selection widgets to the menu
    menu.add.label("Select players:")
    menu.add.selector("Player 1: ", [("Human", "Human_1"), ("AI", "AI_1")], onchange=change_player)
    menu.add.selector("Player 2: ", [("AI", "AI_2"), ("Human", "Human_2")], onchange=change_player)
    menu.add.button("Start game", start_game(screen), screen=screen, accept_kwargs=True)

    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)
    
    # Main loop for the menu
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        menu.mainloop(screen, events)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
