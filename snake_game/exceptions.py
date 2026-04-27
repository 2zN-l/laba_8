class SnakeGameError(Exception):
    """Базовое исключение для игры Змейка."""
    pass

class SnakeCollisionError(SnakeGameError):
    """Исключение при столкновении змейки (с собой или со стеной)."""
    pass

class InvalidDirectionError(SnakeGameError):
    """Исключение при попытке движения в противоположном направлении."""
    pass

class GameOverError(SnakeGameError):
    """Исключение при завершении игры."""
    pass