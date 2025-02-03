import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 0, 128)   # Purple
]

# Game dimensions
BLOCK_SIZE = 35  # Increased block size
GRID_WIDTH = 10
GRID_HEIGHT = 20
PREVIEW_WIDTH = 6
SCREEN_WIDTH = BLOCK_SIZE * (PREVIEW_WIDTH + GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Upside-Down Tetris')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.next_pieces = [self.create_piece() for _ in range(3)]  # Store next 3 pieces
        self.current_piece = self.get_next_piece()
        self.game_over = False
        self.score = 0
        self.speed = 30
        self.counter = 0

    def create_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {
            'shape': shape,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': GRID_HEIGHT - len(shape),
            'color': color
        }

    def get_next_piece(self):
        next_piece = self.next_pieces.pop(0)
        self.next_pieces.append(self.create_piece())
        return next_piece

    def valid_move(self, piece, x, y):
        for row in range(len(piece['shape'])):
            for col in range(len(piece['shape'][0])):
                if piece['shape'][row][col]:
                    if (x + col < 0 or x + col >= GRID_WIDTH or
                        y + row < 0 or y + row >= GRID_HEIGHT or
                        self.grid[y + row][x + col]):
                        return False
        return True

    def merge_piece(self):
        for row in range(len(self.current_piece['shape'])):
            for col in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][row][col]:
                    self.grid[self.current_piece['y'] + row][self.current_piece['x'] + col] = self.current_piece['color']

    def clear_lines(self):
        lines_cleared = 0
        for row in range(GRID_HEIGHT):
            if all(self.grid[row]):
                del self.grid[row]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        return lines_cleared

    def rotate_piece(self):
        shape = self.current_piece['shape']
        rotated = [[shape[j][i] for j in range(len(shape)-1, -1, -1)]
                  for i in range(len(shape[0]))]

        if self.valid_move({'shape': rotated,
                           'x': self.current_piece['x'],
                           'y': self.current_piece['y']},
                          self.current_piece['x'],
                          self.current_piece['y']):
            self.current_piece['shape'] = rotated

    def draw_preview_pieces(self):
        preview_x = BLOCK_SIZE
        for idx, piece in enumerate(self.next_pieces):
            preview_y = BLOCK_SIZE * (idx * 4 + 1)

            # Draw preview box
            pygame.draw.rect(self.screen, GRAY,
                           [preview_x - 5,
                            preview_y - 5,
                            BLOCK_SIZE * 5 + 10,
                            BLOCK_SIZE * 3 + 10], 1)

            # Draw piece
            for row in range(len(piece['shape'])):
                for col in range(len(piece['shape'][0])):
                    if piece['shape'][row][col]:
                        pygame.draw.rect(self.screen,
                                       piece['color'],
                                       [preview_x + col * BLOCK_SIZE,
                                        preview_y + row * BLOCK_SIZE,
                                        BLOCK_SIZE - 1,
                                        BLOCK_SIZE - 1])

    def run(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_a:  # Left
                        if self.valid_move(self.current_piece,
                                         self.current_piece['x'] - 1,
                                         self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_d:  # Right
                        if self.valid_move(self.current_piece,
                                         self.current_piece['x'] + 1,
                                         self.current_piece['y']):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_s:  # Rotate
                        self.rotate_piece()
                    elif event.key == pygame.K_w:  # Speed up
                        self.speed = 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.speed = 30

            if not self.game_over:
                # Move piece up
                self.counter += 1
                if self.counter >= self.speed:
                    self.counter = 0
                    if self.valid_move(self.current_piece,
                                     self.current_piece['x'],
                                     self.current_piece['y'] - 1):
                        self.current_piece['y'] -= 1
                    else:
                        self.merge_piece()
                        lines = self.clear_lines()
                        self.score += lines * 100
                        self.current_piece = self.get_next_piece()
                        if not self.valid_move(self.current_piece,
                                             self.current_piece['x'],
                                             self.current_piece['y']):
                            self.game_over = True

            # Drawing
            self.screen.fill(BLACK)

            # Draw game border
            pygame.draw.rect(self.screen, GRAY,
                           [PREVIEW_WIDTH * BLOCK_SIZE,
                            0,
                            GRID_WIDTH * BLOCK_SIZE,
                            GRID_HEIGHT * BLOCK_SIZE], 2)

            # Draw preview pieces
            self.draw_preview_pieces()

            # Draw grid
            for row in range(GRID_HEIGHT):
                for col in range(GRID_WIDTH):
                    if self.grid[row][col]:
                        pygame.draw.rect(self.screen,
                                       self.grid[row][col],
                                       [(col + PREVIEW_WIDTH) * BLOCK_SIZE,
                                        row * BLOCK_SIZE,
                                        BLOCK_SIZE - 1,
                                        BLOCK_SIZE - 1])

            # Draw current piece
            if not self.game_over:
                for row in range(len(self.current_piece['shape'])):
                    for col in range(len(self.current_piece['shape'][0])):
                        if self.current_piece['shape'][row][col]:
                            pygame.draw.rect(self.screen,
                                           self.current_piece['color'],
                                           [(self.current_piece['x'] + PREVIEW_WIDTH + col) * BLOCK_SIZE,
                                            (self.current_piece['y'] + row) * BLOCK_SIZE,
                                            BLOCK_SIZE - 1,
                                            BLOCK_SIZE - 1])

            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, ((PREVIEW_WIDTH + GRID_WIDTH) * BLOCK_SIZE + 10, 10))

            # Draw controls
            controls = [
                "Controls:",
                "W - Speed Up",
                "A - Move Left",
                "S - Rotate",
                "D - Move Right"
            ]
            for i, text in enumerate(controls):
                control_text = font.render(text, True, WHITE)
                self.screen.blit(control_text,
                               ((PREVIEW_WIDTH + GRID_WIDTH) * BLOCK_SIZE + 10,
                                100 + i * 30))

            if self.game_over:
                game_over_text = font.render('GAME OVER', True, WHITE)
                self.screen.blit(game_over_text,
                               ((PREVIEW_WIDTH + GRID_WIDTH) * BLOCK_SIZE + 10, 50))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Tetris()
    game.run()
    pygame.quit()
