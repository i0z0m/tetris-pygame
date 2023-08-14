import pygame
import random
import time

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
        self.game_over = False
        self.quit_game = False

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

    def draw_prediction_outline(self, surface, block, y_offset):
        for row, line in enumerate(block.shape[block.rotation]):
            for col, char in enumerate(line):
                if char == '0':
                    pygame.draw.rect(surface, COLORS[block.color], ((block.x + col) * BLOCK_SIZE, (block.y + row + y_offset) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.draw_grid(surface)
        self.draw_block(surface, self.current_block)

        # 予測地点の描画
        y_offset = self.predict_fall(self.current_block)
        self.draw_prediction_outline(surface, self.current_block, y_offset)

    def move_block(self, direction):
        if direction == 'left':
            if self.is_valid_move(self.current_block, x_offset=-1):
                self.current_block.move_left()
        elif direction == 'right':
            if self.is_valid_move(self.current_block, x_offset=1):
                self.current_block.move_right()

    def soft_drop(self):
        if self.is_valid_move(self.current_block, y_offset=1):
            self.current_block.move_down()

    def hard_drop(self):
        while self.is_valid_move(self.current_block, y_offset=1):
            self.current_block.move_down()
        self.place_block(self.current_block)
        full_lines = self.check_lines()
        if full_lines:
            self.clear_lines(full_lines)
        self.current_block = self.create_new_block()

    def predict_fall(self, block):
        y_offset = 0
        while self.is_valid_move(block, y_offset=y_offset + 1):
            y_offset += 1
        return y_offset

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
                self.game_over = True

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        soft_drop_speed = 8
        normal_tick_rate = 2
        clock = pygame.time.Clock()

        while not self.game_over:
            while not self.game_over:
                tick_rate = normal_tick_rate
                keys = pygame.key.get_pressed() # 押されているキーを取得
                if keys[pygame.K_DOWN]: # 下キーが押されているかチェック
                    self.move_block('down')
                    tick_rate += soft_drop_speed # 落下速度を早める
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_over = True
                        self.quit_game = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move_block('left')
                        elif event.key == pygame.K_RIGHT:
                            self.move_block('right')
                        elif event.key == pygame.K_UP:
                            self.rotate_block()
                        elif event.key == pygame.K_SPACE: # スペースキーが押されたとき
                            self.hard_drop() # ブロックを一気に下に落とす

                self.update()
                self.draw(screen)
                pygame.display.flip()
                clock.tick(tick_rate)
        if not self.quit_game:
            font = pygame.font.Font(None, 36)
            game_over_text = font.render('Game Over', True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect)
            pygame.display.flip()
            time.sleep(3)

        pygame.quit()



# テトリスのゲームの実行
if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()
