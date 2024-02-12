import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 600  # Update screen dimensions
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Define colors
WHITE = (240, 240, 240)
BLACK = (25, 25, 25)
BACKGROUND = (75, 75, 75)  # Define background color
WHITE_SQUARE_COLOR = (240, 217, 181)
BLACK_SQUARE_COLOR = (181, 136, 99)


PROMOTION_MENU_WIDTH = SQUARE_SIZE * 2
PROMOTION_MENU_HEIGHT = SQUARE_SIZE / 2
PROMOTION_MENU_BG_COLOR = (0, 0, 0, 128)

# Create the display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load chess piece images
piece_images = {}
for piece in ['b_bishop', 'b_pawn', 'b_king', 'b_queen', 'b_rook', 'b_knight',
              'w_king', 'w_queen', 'w_rook', 'w_knight', 'w_bishop', 'w_pawn']:
    #put your own file path for images
    image = pygame.image.load(os.path.join("C:/Users/Desktop/chess_game", f"{piece}.png"))
    piece_images[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

# Define the initial board state
initial_board = [["Empty" for _ in range(COLS)] for _ in range(ROWS)]
move_made = False

# Create a function to draw the board
def draw_board(screen, board, images, selected_row, selected_col, valid_moves, promotion_menu=None):
    screen.fill((255, 255, 255))
    for row in range(len(board)):
        for col in range(len(board[row])):
            # Draw the board squares
            square_color = (238, 238, 210) if (row + col) % 2 == 0 else (118, 150, 86)
            pygame.draw.rect(screen, square_color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw the pieces
            piece = board[row][col]
            if piece is not None:
                image_name = f"{piece.color[0]}_{piece.__class__.__name__.lower()}"
                screen.blit(images[image_name], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    if promotion_menu:
        promotion_menu.draw(screen)


    if selected_row is not None and selected_col is not None:
        piece = board[selected_row][selected_col]
        if piece is not None:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            image_name = f"{piece.color}_{type(piece).__name__.lower()}"
            screen.blit(images[image_name], (selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE))

            if valid_moves is not None:
                for move in valid_moves:
                    move_row, move_col = move
                    pygame.draw.circle(screen, (255, 0, 0), (move_col * SQUARE_SIZE + SQUARE_SIZE // 2, move_row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)



class Piece:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, board, row, col):
        raise NotImplementedError()

    def is_valid_move(self, board, start_row, start_col, end_row, end_col):
        if end_row < 0 or end_row >= len(board) or end_col < 0 or end_col >= len(board[0]):
            return False

        destination_piece = board[end_row][end_col]
        if destination_piece is not None and destination_piece.color == self.color:
            return False

        return True

class Pawn(Piece):
    def valid_moves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'w' else 1
        if (self.color == 'w' and row == 6) or (self.color == 'b' and row == 1):
            if 0 <= row + 2 * direction < 8 and board[row + 2 * direction][col] is None and board[row + direction][col] is None:
                moves.append((row + 2 * direction, col))

        if row + direction >= 0 and row + direction < len(board):
            if board[row + direction][col] is None:
                moves.append((row + direction, col))

            if col - 1 >= 0 and board[row + direction][col - 1] is not None and board[row + direction][col - 1].color != self.color:
                moves.append((row + direction, col - 1))

            if col + 1 < len(board[0]) and board[row + direction][col + 1] is not None and board[row + direction][col + 1].color != self.color:
                moves.append((row + direction, col + 1))

        return moves

class Knight(Piece):
    def valid_moves(self, board, row, col):
        moves = []
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for offset in offsets:
            end_row, end_col = row + offset[0], col + offset[1]
            if self.is_valid_move(board, row, col, end_row, end_col):
                moves.append((end_row, end_col))

        return moves

class Rook(Piece):
    def valid_moves(self, board, row, col):
        moves = []

        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            current_row, current_col = row + direction[0], col + direction[1]

            while self.is_valid_move(board, row, col, current_row, current_col):
                moves.append((current_row, current_col))

                if board[current_row][current_col] is not None:
                    break

                current_row += direction[0]
                current_col += direction[1]

        return moves

class Bishop(Piece):
    def valid_moves(self, board, row, col):
        moves = []

        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            current_row, current_col = row + direction[0], col + direction[1]

            while self.is_valid_move(board, row, col, current_row, current_col):
                moves.append((current_row, current_col))

                if board[current_row][current_col] is not None:
                    break

                current_row += direction[0]
                current_col += direction[1]

        return moves

class Queen(Piece):
    def valid_moves(self, board, row, col):
        moves = []

        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            current_row, current_col = row + direction[0], col + direction[1]

            while self.is_valid_move(board, row, col, current_row, current_col):
                moves.append((current_row, current_col))

                if board[current_row][current_col] is not None:
                    break

                current_row += direction[0]
                current_col += direction[1]

        return moves

class King(Piece):
    def valid_moves(self, board, row, col):
        moves = []

        if (self.color == 'w' and row == 7 and col == 4) or (self.color == 'b' and row == 0 and col == 4):
            rook = board[row][7]
            if isinstance(rook, Rook) and rook.color == self.color:
                if board[row][5] is None and board[row][6] is None:
                    moves.append((row, 6))

        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            end_row, end_col = row + direction[0], col + direction[1]
            if self.is_valid_move(board, row, col, end_row, end_col):
                moves.append((end_row, end_col))

        return moves



def initialize_board():
    board = [
        [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')],
        [Pawn('b') for _ in range(8)],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [Pawn('w') for _ in range(8)],
        [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')]
    ]
    return board

def get_board_position(x, y):
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def draw_highlights(screen, moves, images):
    for move in moves:
        row, col = move
        square_color = (255, 255, 0, 100)
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(square_color)
        screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def show_promotion_menu(screen, x, y, color):
    font = pygame.font.Font(None, 36)
    pieces = ['Queen', 'Rook', 'Bishop', 'Knight']
    rect_width = 100
    rect_height = 30
    rect_gap = 10

    while True:
        for i, piece in enumerate(pieces):
            rect = pygame.Rect(x, y + i * (rect_height + rect_gap), rect_width, rect_height)
            pygame.draw.rect(screen, (200, 200, 200), rect)
            text = font.render(piece, True, (0, 0, 0))
            screen.blit(text, rect.move(5, 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, piece in enumerate(pieces):
                    rect = pygame.Rect(x, y + i * (rect_height + rect_gap), rect_width, rect_height)
                    if rect.collidepoint(mouse_x, mouse_y):
                        return f"{color}_{piece.lower()}"

    return None


class PromotionMenu:
    def __init__(self, x, y, color):
        self.x = x - PROMOTION_MENU_WIDTH // 2
        self.y = y - PROMOTION_MENU_HEIGHT // 2
        self.color = color
        self.options = ['queen', 'rook', 'bishop', 'knight']
        self.pieces = [Queen(color), Rook(color), Bishop(color), Knight(color)]
        self.selected = None

    def draw(self, screen):
        # Draw the background rectangle
        pygame.draw.rect(screen, PROMOTION_MENU_BG_COLOR, (self.x, self.y, PROMOTION_MENU_WIDTH, PROMOTION_MENU_HEIGHT))

        # Draw the individual squares and pieces
        for i, piece in enumerate(self.pieces):
            square_color = WHITE_SQUARE_COLOR if (i % 2) == 0 else BLACK_SQUARE_COLOR
            pygame.draw.rect(screen, square_color, (self.x + (i * SQUARE_SIZE), self.y, SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(piece_images[f"{self.color}_{self.options[i]}"], (self.x + (i * SQUARE_SIZE), self.y))


    def handle_click(self, x, y):
        if self.x <= x <= self.x + PROMOTION_MENU_WIDTH and self.y <= y <= self.y + PROMOTION_MENU_HEIGHT:
            selected_index = (x - self.x) // SQUARE_SIZE
            self.selected = self.options[selected_index]
            promoted_piece_name = f'{self.color}_{self.selected}'
            return promoted_piece_name
        return None



    def get_selected_piece(self):
        if self.selected:
            promoted_piece_name = f'{self.color}_{self.selected}'
            return piece_from_name(promoted_piece_name.split('_')[1], self.color)
        return None




def piece_from_name(name, color):
    if name == 'queen':
        return Queen(color)
    elif name == 'rook':
        return Rook(color)
    elif name == 'bishop':
        return Bishop(color)
    elif name == 'knight':
        return Knight(color)
    else:
        return None



def pawn_promotion_needed(board, color):
    for col in range(8):
        if isinstance(board[0][col], Pawn) and board[0][col].color == color:
            return True, 0, col
        if isinstance(board[7][col], Pawn) and board[7][col].color == color:
            return True, 7, col
    return False, None, None

def move_piece_and_check_promotion(board, src, dest):
    board[dest[0]][dest[1]] = board[src[0]][src[1]]
    board[src[0]][src[1]] = None

    if isinstance(board[dest[0]][dest[1]], Pawn) and ((dest[0] == 0 and board[dest[0]][dest[1]].color == 'b') or (dest[0] == 7 and board[dest[0]][dest[1]].color == 'w')):
        return True, dest[0], dest[1]
    else:
        return False, None, None



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    images = piece_images
    board = initialize_board()
    running = True
    current_turn = 'w'
    selected_piece = None
    selected_row, selected_col = None, None
    valid_moves = []
    turn = True
    promotion_menu = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = get_board_position(x, y)

                if promotion_menu:
                    promoted_piece_name = promotion_menu.handle_click(x, y)
                    if promoted_piece_name:
                        promoted_piece = piece_from_name(promoted_piece_name.split('_')[1], current_turn)
                        board[promotion_row][promotion_col] = promoted_piece
                        promotion_menu = None
                        current_turn = 'b' if current_turn == 'w' else 'w'
                    continue

                if selected_piece:
                    move = (row, col)
                    if move in valid_moves:
                        move_piece_and_check_promotion(board, (selected_row, selected_col), move)
                        need_promotion, promotion_row, promotion_col = pawn_promotion_needed(board, current_turn)
                        if need_promotion:
                            promotion_menu = PromotionMenu(x, y, current_turn)
                        else:
                            current_turn = 'b' if current_turn == 'w' else 'w'
                    selected_piece = None
                    selected_row, selected_col = None, None
                    valid_moves = []
                else:
                    selected_piece = board[row][col]
                    if selected_piece and selected_piece.color == current_turn:
                        selected_row, selected_col = row, col
                        valid_moves = selected_piece.valid_moves(board, row, col)

        draw_board(screen, board, images, selected_row, selected_col, valid_moves, promotion_menu)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()









