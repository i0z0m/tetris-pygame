import pygame
import random

# テトリスの定数
WIDTH, HEIGHT = 800, 600
PLAY_WIDTH, PLAY_HEIGHT = 300, 600
BLOCK_SIZE = 30

# テトリスのブロックの形状
SHAPES = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],

    [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['0000.',
      '.....',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],

    [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']],

    [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
]

# テトリスのブロックの色
COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 0, 0)
]

# テトリスのブロッククラス
class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0
        self.color = random.randint(1, len(COLORS) - 1)

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

# テトリスのゲームクラス
class Tetris:
    def __init__(self):
        self.play_width = PLAY_WIDTH
        self.play_height = PLAY_HEIGHT
        self.grid = [[0] * (self.play_width // BLOCK_SIZE) for _ in range(self.play_height // BLOCK_SIZE)]
        self.current_block = self.create_new_block()

    def create_new_block(self):
        shape = random.choice(SHAPES)
        x = self.play_width // BLOCK_SIZE // 2 - len(shape[0]) // 2
        y = 0
        return Block(x, y, shape)

    def draw_grid(self, surface):
        for y in range(self.play_height // BLOCK_SIZE):
            for x in range(self.play_width // BLOCK_SIZE):
                pygame.draw.rect(surface, COLORS[self.grid[y][x]], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, (128, 128, 128), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_block(self, surface, block):
        for row in range(len(block.shape[block.rotation])):
            for col in range(len(block.shape[block.rotation][row])):
                if block.shape[block.rotation][row][col] == '0':
                    pygame.draw.rect(surface, COLORS[block.color], ((block.x + col) * BLOCK_SIZE, (block.y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, (128, 128, 128), ((block.x + col) * BLOCK_SIZE, (block.y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.draw_grid(surface)
        self.draw_block(surface, self.current_block)

    def move_block(self, direction):
        if direction == 'left':
            if self.is_valid_move(self.current_block, x_offset=-1):
                self.current_block.move_left()
        elif direction == 'right':
            if self.is_valid_move(self.current_block, x_offset=1):
                self.current_block.move_right()
        elif direction == 'down':
            if self.is_valid_move(self.current_block, y_offset=1):
                self.current_block.move_down()

    def rotate_block(self):
        temp_rotation = self.current_block.rotation
        self.current_block.rotate()
        if not self.is_valid_move(self.current_block):
            self.current_block.rotation = temp_rotation

    def is_valid_move(self, block, x_offset=0, y_offset=0):
        for row in range(len(block.shape[block.rotation])):
            for col in range(len(block.shape[block.rotation][row])):
                if block.shape[block.rotation][row][col] == '0':
                    x = block.x + col + x_offset
                    y = block.y + row + y_offset
                    if x < 0 or x >= self.play_width // BLOCK_SIZE or y >= self.play_height // BLOCK_SIZE or self.grid[y][x] != 0:
                        return False
        return True

    def place_block(self, block):
        for row in range(len(block.shape[block.rotation])):
            for col in range(len(block.shape[block.rotation][row])):
                if block.shape[block.rotation][row][col] == '0':
                    x = block.x + col
                    y = block.y + row
                    self.grid[y][x] = block.color

    def check_lines(self):
        full_lines = []
        for row in range(len(self.grid)):
            if all(self.grid[row]):
                full_lines.append(row)
        return full_lines

    def clear_lines(self, lines):
        for line in lines:
            del self.grid[line]
            self.grid.insert(0, [0] * (self.play_width // BLOCK_SIZE))

    def update(self):
        if self.is_valid_move(self.current_block, y_offset=1):
            self.current_block.move_down()
        else:
            self.place_block(self.current_block)
            full_lines = self.check_lines()
            if full_lines:
                self.clear_lines(full_lines)
            self.current_block = self.create_new_block()
            if not self.is_valid_move(self.current_block):
                # ゲームオーバーの処理
                pass

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_block('left')
                    elif event.key == pygame.K_RIGHT:
                        self.move_block('right')
                    elif event.key == pygame.K_DOWN:
                        self.move_block('down')
                    elif event.key == pygame.K_UP:
                        self.rotate_block()

            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()


# テトリスのゲームの実行
if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()
