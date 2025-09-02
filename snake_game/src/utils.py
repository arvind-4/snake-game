"""Utility functions for the Snake Game."""

import contextlib
import secrets
import tkinter as tk
from tkinter import messagebox

import pygame

from snake_game.src.models import Cube, Snake


def draw_grid(w: int, rows: int) -> None:
    """Draw grid lines on the game surface."""
    sizebtwn: int = w // rows
    x: int = 0
    y: int = 0

    for _ in range(rows):
        x += sizebtwn
        y += sizebtwn


def random_snack(rows: int, snake: Snake) -> tuple[int, int]:
    """Generate a random position for the snack."""
    positions: list[Cube] = snake.body

    while True:
        x: int = secrets.randbelow(rows)
        y: int = secrets.randbelow(rows)

        # Check if the position overlaps with any part of the snake
        if len(list(filter(lambda cube: cube.pos == (x, y), positions))) > 0:
            continue
        break

    return x, y


def message_box(subject: str, context: str) -> None:
    """Display a message box with the given subject and context.

    Args:
        subject: Title of the message box
        context: Content of the message box

    """
    root: tk.Tk = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, context)

    with contextlib.suppress(Exception):
        root.destroy()


def redraw_window(
    surface: pygame.Surface, snake: Snake, snack: Cube, width: int, rows: int
) -> None:
    """Redraw the entire game window.

    Args:
        surface: Pygame surface to draw on
        snake: The snake object to draw
        snack: The snack cube to draw
        width: Width of the game window
        rows: Number of rows in the grid

    """
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows)
    pygame.display.update()
