"""Main game logic for the Snake Game."""

import pygame

from .models import Cube, Snake
from .utils import message_box, random_snack, redraw_window


def main() -> None:
    """Run the main game loop."""
    # Game constants
    width: int = 500
    rows: int = 20

    # Initialize pygame
    pygame.init()
    win: pygame.Surface = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Snake Game")

    # Initialize game objects
    snake: Snake = Snake((255, 0, 0), (10, 10))
    snack: Cube = Cube(random_snack(rows, snake), color=(0, 255, 0))
    clock: pygame.time.Clock = pygame.time.Clock()

    # Game loop
    running: bool = True
    while running:
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input
        keys = pygame.key.get_pressed()
        snake.handle_input(keys)

        # Game timing
        pygame.time.delay(125)
        clock.tick(20)

        # Move snake
        snake.move()

        # Check if snake ate the snack
        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(rows, snake), color=(0, 255, 0))

        # Check for self-collision
        for x in range(len(snake.body)):
            if snake.body[x].pos in [cube.pos for cube in snake.body[x + 1 :]]:
                score: int = len(snake.body)
                message_box("You Lost!", f"Your Score: {score}. Play Again?")
                snake.reset((10, 10))
                break

        # Redraw everything
        redraw_window(win, snake, snack, width, rows)

    pygame.quit()


if __name__ == "__main__":
    main()
