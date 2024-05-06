# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def show_end_screen(win, message):
    run = True
    font = pygame.font.SysFont('comicsansms', 40)  # A stylish font

    # Draw a gradient rectangle
    def draw_gradient_rect(window, rect, color_from, color_to):
        height = rect.height
        top_color = color_from
        bottom_color = color_to
        step = [(y - x) / height for x, y in zip(top_color, bottom_color)]
        for y in range(rect.top, rect.top + height):
            color = [int(x + step[i] * (y - rect.top)) for i, x in enumerate(top_color)]
            pygame.draw.line(window, color, (rect.left, y), (rect.right, y))

    while run:
        win.fill((0, 0, 0))
        draw_gradient_rect(win, pygame.Rect(0, 0, WIDTH, HEIGHT), (23, 32, 42), (44, 62, 80))

        text = font.render(message, True, (255, 200, 100))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)

        new_game_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 70, 220, 60)
        exit_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 150, 220, 60)

        draw_gradient_rect(win, new_game_button, (46, 204, 113), (26, 188, 156))
        draw_gradient_rect(win, exit_button, (231, 76, 60), (192, 57, 43))

        new_game_text = font.render('New Game', True, (255, 255, 255))
        new_game_text_rect = new_game_text.get_rect(center=new_game_button.center)
        win.blit(new_game_text, new_game_text_rect)

        exit_text = font.render('Exit', True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        win.blit(exit_text, exit_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    print("New Game Button Pressed") 
                    return True 
                elif exit_button.collidepoint(event.pos):
                    print("Exit Button Pressed") 
                    pygame.quit()
                    return False

        pygame.time.delay(100)

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        #call AI
        if game.turn == WHITE:
            #Higher the depth(int) the better AI but slower it is
            value, new_board = minimax(game.get_board(), 2 , WHITE, game)
            game.ai_move(new_board)

        winner = game.winner()
        if winner is not None:
            message = 'Red Wins!' if winner == RED else 'White Wins!'
            if not show_end_screen(WIN, message):
                break
            game.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()