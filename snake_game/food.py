import pygame
import random

class Food:
    def __init__(self, cell_size: int = 20):
        self.cell_size = cell_size
        self.position = [0, 0]
        self.color = (255, 50, 50)
    
    def randomize_position(self, width_cells: int, height_cells: int, snake_body: list):
        while True:
            pos = [random.randint(0, width_cells - 1), random.randint(0, height_cells - 1)]
            if pos not in snake_body:
                self.position = pos
                break
    
    def draw(self, screen):
        rect = pygame.Rect(self.position[0] * self.cell_size, self.position[1] * self.cell_size,
                           self.cell_size - 2, self.cell_size - 2)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (255, 150, 150), rect, 2)