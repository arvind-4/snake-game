"""Game models for the Snake Game."""

import pygame


class Cube:
    """Represents a single cube/segment in the game."""

    rows: int = 20
    w: int = 500

    def __init__(
        self,
        start: tuple[int, int],
        dirnx: int = 1,
        dirny: int = 0,
        color: tuple[int, int, int] = (255, 0, 0),
    ) -> None:
        """Initialize a cube.

        Args:
            start: Starting position as (x, y) tuple
            dirnx: Direction in x-axis (-1, 0, or 1)
            dirny: Direction in y-axis (-1, 0, or 1)
            color: RGB color tuple

        """
        self.pos: tuple[int, int] = start
        self.dirnx: int = dirnx
        self.dirny: int = dirny
        self.color: tuple[int, int, int] = color

    def move(self, dirnx: int, dirny: int) -> None:
        """Move the cube in the specified direction.

        Args:
            dirnx: Direction in x-axis
            dirny: Direction in y-axis

        """
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface: pygame.Surface, eyes: bool = False) -> None:
        """Draw the cube on the given surface.

        Args:
            surface: Pygame surface to draw on
            eyes: Whether to draw eyes (for snake head)

        """
        dis: int = self.w // self.rows
        i, j = self.pos[0], self.pos[1]

        pygame.draw.rect(
            surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2)
        )

        if eyes:
            centre: int = dis // 2
            radius: int = 3
            circle_middle: tuple[int, int] = (i * dis + centre - radius, j * dis + 8)
            circle_middle2: tuple[int, int] = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake:
    """Represents the snake in the game."""

    def __init__(self, color: tuple[int, int, int], pos: tuple[int, int]) -> None:
        """Initialize the snake.

        Args:
            color: RGB color tuple for the snake
            pos: Starting position as (x, y) tuple

        """
        self.color: tuple[int, int, int] = color
        self.head: Cube = Cube(pos)
        self.body: list[Cube] = [self.head]
        self.turns: dict[tuple[int, int], list[int]] = {}
        self.dirnx: int = 0
        self.dirny: int = 1

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle keyboard input for snake direction."""
        try:
            if keys[pygame.K_LEFT] and self.dirnx != 1:  # Prevent going backwards
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT] and self.dirnx != -1:  # Prevent going backwards
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP] and self.dirny != 1:  # Prevent going backwards
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN] and self.dirny != -1:  # Prevent going backwards
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        except (KeyError, TypeError):
            pass

    def move(self) -> None:
        """Move the snake based on current direction and turns."""
        for i, c in enumerate(self.body):
            p: tuple[int, int] = c.pos[:]
            if p in self.turns:
                turn: list[int] = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            elif c.dirnx == -1 and c.pos[0] <= 0:
                c.pos = (c.rows - 1, c.pos[1])
            elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                c.pos = (0, c.pos[1])
            elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                c.pos = (c.pos[0], 0)
            elif c.dirny == -1 and c.pos[1] <= 0:
                c.pos = (c.pos[0], c.rows - 1)
            else:
                c.move(c.dirnx, c.dirny)

    def reset(self, pos: tuple[int, int]) -> None:
        """Reset the snake to initial state.

        Args:
            pos: Starting position as (x, y) tuple

        """
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self) -> None:
        """Add a new cube to the snake's body."""
        tail: Cube = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the snake on the given surface.

        Args:
            surface: Pygame surface to draw on

        """
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
