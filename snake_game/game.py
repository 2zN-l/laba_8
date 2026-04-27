import pygame
import sys
from .snake import Snake
from .food import Food
from .exceptions import SnakeCollisionError, GameOverError

class SnakeGame:
    """Основной класс игры."""
    
    def __init__(self, width: int = 800, height: int = 600, cell_size: int = 20):
        pygame.init()
        
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.width_cells = width // cell_size
        self.height_cells = height // cell_size
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("🐍 Змейка - Вариант 10")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.score = 0
        self.high_score = self._load_high_score()
        self.running = False
        
        self._init_game_objects()
    
    def _init_game_objects(self):
        start_pos = [self.width_cells // 2, self.height_cells // 2]
        self.snake = Snake(start_pos, self.cell_size)
        self.food = Food(self.cell_size)
        self.food.randomize_position(self.width_cells, self.height_cells, self.snake.body)
    
    def _load_high_score(self) -> int:
        try:
            with open("snake_score.txt", "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0
    
    def _save_high_score(self):
        with open("snake_score.txt", "w") as f:
            f.write(str(self.high_score))
    
    def _teleport_if_needed(self, pos: list) -> list:
        """Телепортирует змейку через границы экрана."""
        new_pos = pos.copy()
        
        if new_pos[0] < 0:
            new_pos[0] = self.width_cells - 1
        elif new_pos[0] >= self.width_cells:
            new_pos[0] = 0
        
        if new_pos[1] < 0:
            new_pos[1] = self.height_cells - 1
        elif new_pos[1] >= self.height_cells:
            new_pos[1] = 0
        
        return new_pos
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(Snake.UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(Snake.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(Snake.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(Snake.RIGHT)
                elif event.key == pygame.K_SPACE and not self.running:
                    self.restart()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def _update(self):
        if not self.running:
            return
        
        self.snake.move()
        
        # Проверяем и телепортируем голову змейки
        head = self.snake.head
        teleported_head = self._teleport_if_needed(head)
        
        # Если голова телепортировалась, обновляем позицию
        if teleported_head != head:
            self.snake.body[0] = teleported_head
        
        # Проверка столкновения с собой (но не со стенами - их нет)
        if self.snake.check_self_collision():
            raise SnakeCollisionError("Змейка врезалась в себя!")
        
        # Проверка поедания еды
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
            self.food.randomize_position(self.width_cells, self.height_cells, self.snake.body)
    
    def _draw(self):
        self.screen.fill((0, 0, 0))
        
        # Рисуем сетку (опционально)
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
            
            if self.score > 0:
                game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, (255, 50, 50))
                score_text = self.font.render(f"Ваш счёт: {self.score}", True, (255, 255, 255))
                restart_text = self.small_font.render("Нажмите ПРОБЕЛ для новой игры", True, (255, 255, 255))
                exit_text = self.small_font.render("Нажмите ESC для выхода", True, (200, 200, 200))
            else:
                game_over_text = self.font.render("ЗМЕЙКА", True, (50, 200, 50))
                restart_text = self.small_font.render("Нажмите ПРОБЕЛ для начала", True, (255, 255, 255))
                exit_text = self.small_font.render("Нажмите ESC для выхода", True, (200, 200, 200))
                score_text = self.small_font.render("Управление: стрелки", True, (255, 255, 255))
            
            self.screen.blit(game_over_text, (self.width//2 - game_over_text.get_width()//2, self.height//2 - 60))
            self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2 - 10))
            self.screen.blit(restart_text, (self.width//2 - restart_text.get_width()//2, self.height//2 + 40))
            self.screen.blit(exit_text, (self.width//2 - exit_text.get_width()//2, self.height//2 + 80))
        
        pygame.display.flip()
    
    def run(self):
        self.running = True
        
        while self.running:
            try:
                self._handle_input()
                self._update()
                self._draw()
                self.clock.tick(10)
            except SnakeCollisionError:
                self.running = False
            except Exception as e:
                print(f"Ошибка: {e}")
                self.running = False
        
        self._draw()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
        
        pygame.quit()
        sys.exit()
    
    def restart(self):
        self.score = 0
        self._init_game_objects()
        self.running = True