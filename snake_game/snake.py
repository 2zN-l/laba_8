import pygame
from .exceptions import InvalidDirectionError

class Snake:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    def __init__(self, start_pos: list, cell_size: int = 20):
        self.cell_size = cell_size
        self.body = [start_pos.copy()]
        self.direction = self.RIGHT
        self.grow_flag = False
    
    @property
    def head(self) -> list:
        return self.body[0]
    
    def change_direction(self, new_direction: tuple):
        if (new_direction[0] == -self.direction[0] and 
            new_direction[1] == -self.direction[1]):
            raise InvalidDirectionError("Нельзя повернуть назад")
        self.direction = new_direction
    
    def move(self):
        head = self.head
        new_head = [head[0] + self.direction[0], head[1] + self.direction[1]]
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        self.grow_flag = True
    
    def check_self_collision(self) -> bool:
        return self.head in self.body[1:]
    
    def draw(self, screen):
        # Рисуем тело змейки
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] * self.cell_size,
                segment[1] * self.cell_size,
                self.cell_size - 2,
                self.cell_size - 2
            )
            pygame.draw.rect(screen, (0, 150, 0), rect)
            pygame.draw.rect(screen, (0, 200, 0), rect, 2)
        
        # Рисуем голову
        head_rect = pygame.Rect(
            self.head[0] * self.cell_size,
            self.head[1] * self.cell_size,
            self.cell_size - 2,
            self.cell_size - 2
        )
        pygame.draw.rect(screen, (0, 200, 0), head_rect)
        
        # ========== ГЛАЗКИ ==========
        eye_size = max(3, self.cell_size // 6)
        
        # Определяем положение глаз в зависимости от направления
        if self.direction == self.RIGHT:
            eye1 = (head_rect.x + head_rect.width - eye_size, head_rect.y + eye_size)
            eye2 = (head_rect.x + head_rect.width - eye_size, head_rect.y + head_rect.height - eye_size*2)
        elif self.direction == self.LEFT:
            eye1 = (head_rect.x + 2, head_rect.y + eye_size)
            eye2 = (head_rect.x + 2, head_rect.y + head_rect.height - eye_size*2)
        elif self.direction == self.UP:
            eye1 = (head_rect.x + eye_size, head_rect.y + 2)
            eye2 = (head_rect.x + head_rect.width - eye_size*2, head_rect.y + 2)
        else:  # DOWN
            eye1 = (head_rect.x + eye_size, head_rect.y + head_rect.height - 4)
            eye2 = (head_rect.x + head_rect.width - eye_size*2, head_rect.y + head_rect.height - 4)
        
        # Белки глаз
        pygame.draw.circle(screen, (255, 255, 255), eye1, eye_size)
        pygame.draw.circle(screen, (255, 255, 255), eye2, eye_size)
        # Зрачки
        pygame.draw.circle(screen, (0, 0, 0), eye1, eye_size // 2)
        pygame.draw.circle(screen, (0, 0, 0), eye2, eye_size // 2)