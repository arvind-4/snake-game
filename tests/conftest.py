"""
Pytest configuration and fixtures for snake_game tests.
"""

import pytest
import pygame
import os
from unittest.mock import Mock


@pytest.fixture(scope="session", autouse=True)
def setup_pygame():
    """Setup pygame for testing session."""
    # Set SDL to use dummy video driver for headless testing
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def pygame_surface():
    """Provide a pygame surface for testing."""
    return pygame.Surface((500, 500))


@pytest.fixture
def mock_pygame_keys():
    """Provide a mock pygame keys object."""
    keys = Mock()
    keys.__getitem__ = Mock(return_value=False)
    # Add pygame key constants for testing
    keys.__contains__ = Mock(return_value=True)
    return keys


@pytest.fixture
def mock_pygame_keys_pressed():
    """Provide a mock pygame keys object that simulates key presses."""
    def key_pressed(key):
        # Return False for all keys by default
        return False

    keys = Mock()
    keys.__getitem__ = Mock(side_effect=key_pressed)
    return keys


@pytest.fixture
def sample_snake():
    """Provide a sample snake for testing."""
    from snake_game.src.models import Snake
    return Snake((255, 0, 0), (10, 10))


@pytest.fixture
def sample_cube():
    """Provide a sample cube for testing."""
    from snake_game.src.models import Cube
    return Cube((5, 5), color=(0, 255, 0))


@pytest.fixture
def multi_segment_snake():
    """Provide a snake with multiple segments for testing."""
    from snake_game.src.models import Snake
    snake = Snake((255, 0, 0), (10, 10))
    for _ in range(3):
        snake.add_cube()
    return snake


@pytest.fixture(autouse=True)
def reset_pygame_state():
    """Reset pygame state between tests."""
    yield
    # Clean up any pygame state if needed
    if pygame.get_init():
        pygame.event.clear()


@pytest.fixture
def mock_tkinter_root():
    """Provide a mock tkinter root for testing."""
    root = Mock()
    root.attributes = Mock()
    root.withdraw = Mock()
    root.destroy = Mock()
    return root
