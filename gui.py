import pygame
import sys
from pygame.locals import *
from tictactoe import TicTacToe
from player import AIPlayer

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
ROWS = 7
COLS = 7
SQUARE_SIZE = SCREEN_WIDTH // COLS
LINE_WIDTH = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def draw_board(screen, game):
    # Draw the grid lines
    for i in range(1, COLS):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SCREEN_HEIGHT), LINE_WIDTH)
    for i in range(1, ROWS):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (SCREEN_WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

    # Draw X's and O's
    for row in range(ROWS):
        for col in range(COLS):
            mark = game.board[row][col]
            if mark == 1:  # X
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE), LINE_WIDTH)
            elif mark == -1:  # O
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - LINE_WIDTH, LINE_WIDTH)

def show_dialog(screen, winner):
    font = pygame.font.Font(None, 36)
    if winner == "Tie":
        text_surface = font.render(f"Tie", True, BLACK)
    else:
        text_surface = font.render(f"{winner} wins!", True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    next_button = pygame.Rect(100, 300, 100, 50)
    quit_button = pygame.Rect(220, 300, 100, 50)

    pygame.draw.rect(screen, GREEN, next_button)
    pygame.draw.rect(screen, RED, quit_button)

    font = pygame.font.Font(None, 24)
    next_text = font.render("Next", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)

    screen.blit(next_text, next_button.center)
    screen.blit(quit_text, quit_button.center)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if next_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")

    clock = pygame.time.Clock()
    running = True

    while running:
        game = TicTacToe(n=ROWS, winning_condition=5)
        player_1 = AIPlayer(1)
        player_2 = AIPlayer(-1)
        draw_board(screen, game)

        while not game.check_game_over()[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                
            # check player turn
            if game.current_turn == 1:
                player = player_1 
            else:
                player = player_2
                
            action = player.get_move(game)
            print(f"{game.current_turn}: {action}")
            game.move(action)
            screen.fill(WHITE)
            draw_board(screen, game)
            pygame.display.flip()
        
        winner_mask = game.check_game_over()[1]
        if winner_mask > 0:
            winner = "Player 1"
        elif winner_mask < 0:
            winner = "Player 2"
        else:
            winner = "Tie"
        restart = show_dialog(screen, winner)
        
        clock.tick(60)  # Limit to 60 FPS

        if not restart:
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
