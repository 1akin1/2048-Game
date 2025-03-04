import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
TILE_SIZE = 80
GRID_PADDING = 10
FONT_SIZE = 36
ANIMATION_SPEED = 15

# Colors - Updated with a new dark theme
BACKGROUND_COLOR = (40, 44, 52)
EMPTY_TILE_COLOR = (60, 64, 72)
TILE_COLORS = {
    0: (60, 64, 72),
    2: (78, 90, 115),
    4: (95, 129, 157),
    8: (124, 153, 180),
    16: (141, 175, 199),
    32: (152, 195, 121),
    64: (229, 192, 123),
    128: (224, 108, 117),
    256: (198, 120, 221),
    512: (171, 178, 191),
    1024: (130, 170, 255),
    2048: (255, 135, 135)
}
TEXT_COLORS = {
    2: (220, 223, 228),
    4: (220, 223, 228),
    8: (220, 223, 228),
    16: (220, 223, 228),
    32: (220, 223, 228),
    64: (220, 223, 228),
    128: (220, 223, 228),
    256: (220, 223, 228),
    512: (220, 223, 228),
    1024: (220, 223, 228),
    2048: (220, 223, 228)
}

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
small_font = pygame.font.SysFont("Arial", 24)

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.animations = []  # List to store animations
        self.add_new_tile()
        self.add_new_tile()
    
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            # Add animation for new tile (scale from 0 to 1)
            self.animations.append({
                'type': 'new',
                'row': i,
                'col': j,
                'progress': 0,
                'duration': 10
            })
    
    def move(self, direction):
        if self.game_over:
            return False
        
        moved = False
        if direction == "up":
            moved = self.move_up()
        elif direction == "down":
            moved = self.move_down()
        elif direction == "left":
            moved = self.move_left()
        elif direction == "right":
            moved = self.move_right()
        
        if moved:
            self.add_new_tile()
            self.check_game_over()
        
        return moved
    
    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                if self.grid[i][j] != 0:
                    k = j
                    while k > 0 and self.grid[i][k-1] == 0:
                        self.grid[i][k-1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k -= 1
                        moved = True
                        # Add slide animation
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': i,
                            'to_col': k,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k > 0 and self.grid[i][k-1] == self.grid[i][k]:
                        value = self.grid[i][k] * 2
                        self.grid[i][k-1] = value
                        self.score += value
                        self.grid[i][k] = 0
                        moved = True
                        
                        # Add merge animation
                        self.animations.append({
                            'type': 'merge',
                            'row': i,
                            'col': k-1,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        
                        if value == 2048 and not self.won:
                            self.won = True
        
        return moved
    
    def move_right(self):
        moved = False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = j
                    while k < GRID_SIZE-1 and self.grid[i][k+1] == 0:
                        self.grid[i][k+1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k += 1
                        moved = True
                        # Add slide animation
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': i,
                            'to_col': k,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k < GRID_SIZE-1 and self.grid[i][k+1] == self.grid[i][k]:
                        value = self.grid[i][k] * 2
                        self.grid[i][k+1] = value
                        self.score += value
                        self.grid[i][k] = 0
                        moved = True
                        
                        # Add merge animation
                        self.animations.append({
                            'type': 'merge',
                            'row': i,
                            'col': k+1,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        
                        if value == 2048 and not self.won:
                            self.won = True
        
        return moved
    
    def move_up(self):
        moved = False
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                if self.grid[i][j] != 0:
                    k = i
                    while k > 0 and self.grid[k-1][j] == 0:
                        self.grid[k-1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k -= 1
                        moved = True
                        # Add slide animation
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': k,
                            'to_col': j,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k > 0 and self.grid[k-1][j] == self.grid[k][j]:
                        value = self.grid[k][j] * 2
                        self.grid[k-1][j] = value
                        self.score += value
                        self.grid[k][j] = 0
                        moved = True
                        
                        # Add merge animation
                        self.animations.append({
                            'type': 'merge',
                            'row': k-1,
                            'col': j,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        
                        if value == 2048 and not self.won:
                            self.won = True
        
        return moved
    
    def move_down(self):
        moved = False
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = i
                    while k < GRID_SIZE-1 and self.grid[k+1][j] == 0:
                        self.grid[k+1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k += 1
                        moved = True
                        # Add slide animation
                        self.animations.append({
                            'type': 'slide',
                            'from_row': i,
                            'from_col': j,
                            'to_row': k,
                            'to_col': j,
                            'progress': 0,
                            'duration': 8
                        })
                    
                    if k < GRID_SIZE-1 and self.grid[k+1][j] == self.grid[k][j]:
                        value = self.grid[k][j] * 2
                        self.grid[k+1][j] = value
                        self.score += value
                        self.grid[k][j] = 0
                        moved = True
                        
                        # Add merge animation
                        self.animations.append({
                            'type': 'merge',
                            'row': k+1,
                            'col': j,
                            'progress': 0,
                            'duration': 8,
                            'value': value
                        })
                        
                        if value == 2048 and not self.won:
                            self.won = True
        
        return moved
    
    def check_game_over(self):
        # Check if there are any empty cells
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        
        # Check if there are any adjacent cells with the same value
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if j < GRID_SIZE-1 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < GRID_SIZE-1 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        
        self.game_over = True
        return True
    
    def reset(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.animations = []
        self.add_new_tile()
        self.add_new_tile()
    
    def update_animations(self):
        # Update all animations
        completed = []
        for i, anim in enumerate(self.animations):
            anim['progress'] += 1
            if anim['progress'] >= anim['duration']:
                completed.append(i)
        
        # Remove completed animations (in reverse order to avoid index issues)
        for i in sorted(completed, reverse=True):
            self.animations.pop(i)

def draw_tile(x, y, value, animations=None):
    # Draw tile background
    color = TILE_COLORS.get(value, TILE_COLORS[2048])
    
    # Apply animations if any
    scale = 1.0
    if animations:
        for anim in animations:
            if anim['type'] == 'new' and value != 0:
                # Scale animation for new tiles
                progress_ratio = anim['progress'] / anim['duration']
                scale = progress_ratio
            elif anim['type'] == 'merge':
                # Pulse animation for merged tiles
                progress_ratio = anim['progress'] / anim['duration']
                if progress_ratio < 0.5:
                    scale = 1.0 + 0.2 * (progress_ratio * 2)
                else:
                    scale = 1.0 + 0.2 * (1 - (progress_ratio - 0.5) * 2)
    
    # Calculate scaled dimensions
    scaled_size = int(TILE_SIZE * scale)
    offset = (TILE_SIZE - scaled_size) // 2
    
    pygame.draw.rect(screen, color, (x + offset, y + offset, scaled_size, scaled_size), border_radius=5)
    
    # Draw tile value
    if value != 0:
        text_color = TEXT_COLORS.get(value, TEXT_COLORS[2048])
        text_size = FONT_SIZE
        if value > 512:
            text_size = FONT_SIZE - 8
        if value > 8192:
            text_size = FONT_SIZE - 16
        
        font = pygame.font.SysFont("Arial", text_size, bold=True)
        text = font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
        screen.blit(text, text_rect)

def draw_grid(game):
    # Draw background
    screen.fill(BACKGROUND_COLOR)
    
    # Draw grid background
    grid_rect = pygame.Rect(GRID_PADDING, 100, WIDTH - 2*GRID_PADDING, WIDTH - 2*GRID_PADDING)
    pygame.draw.rect(screen, (50, 54, 62), grid_rect, border_radius=5)
    
    # Draw empty tile slots
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = GRID_PADDING + j * (TILE_SIZE + GRID_PADDING)
            y = 100 + i * (TILE_SIZE + GRID_PADDING)
            pygame.draw.rect(screen, EMPTY_TILE_COLOR, (x, y, TILE_SIZE, TILE_SIZE), border_radius=5)
    
    # Draw tiles with animations
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if game.grid[i][j] != 0:
                x = GRID_PADDING + j * (TILE_SIZE + GRID_PADDING)
                y = 100 + i * (TILE_SIZE + GRID_PADDING)
                
                # Find animations for this tile
                tile_animations = [a for a in game.animations if 
                                  (a['type'] == 'new' and a['row'] == i and a['col'] == j) or
                                  (a['type'] == 'merge' and a['row'] == i and a['col'] == j)]
                
                draw_tile(x, y, game.grid[i][j], tile_animations)
    
    # Draw slide animations
    for anim in game.animations:
        if anim['type'] == 'slide':
            progress_ratio = anim['progress'] / anim['duration']
            from_x = GRID_PADDING + anim['from_col'] * (TILE_SIZE + GRID_PADDING)
            from_y = 100 + anim['from_row'] * (TILE_SIZE + GRID_PADDING)
            to_x = GRID_PADDING + anim['to_col'] * (TILE_SIZE + GRID_PADDING)
            to_y = 100 + anim['to_row'] * (TILE_SIZE + GRID_PADDING)
            
            x = from_x + (to_x - from_x) * progress_ratio
            y = from_y + (to_y - from_y) * progress_ratio
            
            # Only draw if animation is in progress
            if progress_ratio < 1.0:
                draw_tile(x, y, game.grid[anim['to_row']][anim['to_col']])
    
    # Draw score with a nicer style
    score_bg = pygame.Rect(20, 20, 160, 60)
    pygame.draw.rect(screen, (60, 64, 72), score_bg, border_radius=10)
    score_label = small_font.render("SCORE", True, (171, 178, 191))
    score_text = font.render(f"{game.score}", True, (220, 223, 228))
    screen.blit(score_label, (score_bg.centerx - score_label.get_width()//2, score_bg.y + 10))
    screen.blit(score_text, (score_bg.centerx - score_text.get_width()//2, score_bg.y + 30))
    
    # Draw game over or win message
    if game.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        restart_text = small_font.render("Press R to restart", True, (255, 255, 255))
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))
    
    elif game.won:
        win_text = font.render("You Win!", True, (152, 195, 121))
        continue_text = small_font.render("Keep playing or press R to restart", True, (171, 178, 191))
        
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, 65))
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT - 30))

def main():
    game = Game2048()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")
                elif event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_r:
                    game.reset()
        
        # Update animations
        game.update_animations()
        
        draw_grid(game)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
