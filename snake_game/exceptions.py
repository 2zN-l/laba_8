class SnakeGameError(Exception):
    pass

class SnakeCollisionError(SnakeGameError):
    pass

class InvalidDirectionError(SnakeGameError):
    pass

class GameOverError(SnakeGameError):
    pass