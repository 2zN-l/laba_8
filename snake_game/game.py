import pygame
import sys
import time
from .snake import Snake
from .food import Food
from .exceptions import InvalidDirectionError
from .db import StatsDatabase

class SnakeGame:
    def __init__(self, width: int = 800, height: int = 600, cell_size: int = 20):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.width_cells = width // cell_size
        self.height_cells = height // cell_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("🐍 Змейка")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.score = 0
        self.high_score = self._load_high_score()
        self.running = True
        self.game_start_time = None
        self.db = StatsDatabase()
        self._init_game_objects()
    
    def _init_game_objects(self):
        start_pos = [self.width_cells // 2, self.height_cells // 2]
        self.snake = Snake(start_pos, self.cell_size)
        self.food = Food(self.cell_size)
        self.food.randomize_position(self.width_cells, self.height_cells, self.snake.body)
        self.game_start_time = time.time()
        self.score = 0
    
    def _load_high_score(self) -> int:
        try:
            with open("snake_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def _save_high_score(self):
        try:
            with open("snake_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    try:
                        self.snake.change_direction(Snake.UP)
                    except InvalidDirectionError:
                        pass
                elif event.key == pygame.K_DOWN:
                    try:
                        self.snake.change_direction(Snake.DOWN)
                    except InvalidDirectionError:
                        pass
                elif event.key == pygame.K_LEFT:
                    try:
                        self.snake.change_direction(Snake.LEFT)
                    except InvalidDirectionError:
                        pass
                elif event.key == pygame.K_RIGHT:
                    try:
                        self.snake.change_direction(Snake.RIGHT)
                    except InvalidDirectionError:
                        pass
                elif event.key == pygame.K_SPACE:
                    self.restart()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def _update(self):
        self.snake.move()
        
        head = self.snake.head
        if head[0] < 0 or head[0] >= self.width_cells or head[1] < 0 or head[1] >= self.height_cells:
            self._game_over()
            return
        
        if self.snake.check_self_collision():
            self._game_over()
            return
        
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
            self.food.randomize_position(self.width_cells, self.height_cells, self.snake.body)
    
    def _game_over(self):
        try:

            duration = time.time() - self.game_start_time
            self.db.save_game(self.score, round(duration, 2))
        except Exception as e:
            print(f"Ошибка сохранения в БД: {e}")
        finally:
            self.running = False
    
    def _draw(self):
        self.screen.fill((0, 0, 0))
        
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.width, y))
        
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        score_text = self.font.render(f"Счёт: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        high_text = self.small_font.render(f"Рекорд: {self.high_score}", True, (200, 200, 200))
        self.screen.blit(high_text, (10, 50))
        
        if not self.running:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, (255, 50, 50))
            score_text = self.font.render(f"Ваш счёт: {self.score}", True, (255, 255, 255))
            restart_text = self.small_font.render("Нажмите ПРОБЕЛ для новой игры", True, (255, 255, 255))
            exit_text = self.small_font.render("Нажмите ESC для выхода", True, (200, 200, 200))
            
            self.screen.blit(game_over_text, (self.width//2 - game_over_text.get_width()//2, self.height//2 - 60))
            self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2 - 10))
            self.screen.blit(restart_text, (self.width//2 - restart_text.get_width()//2, self.height//2 + 40))
            self.screen.blit(exit_text, (self.width//2 - exit_text.get_width()//2, self.height//2 + 80))
        
        pygame.display.flip()
    
    def run(self):
        self.running = True
        while self.running:
            self._handle_input()
            self._update()
            self._draw()
            self.clock.tick(10)
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart()
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def restart(self):
        self._init_game_objects()
        self.running = True
        self.run()