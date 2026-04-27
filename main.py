from snake_game.game import SnakeGame

if __name__ == "__main__":
    game = SnakeGame(width=800, height=600, cell_size=20)
    game.run()