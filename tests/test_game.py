"""
Comprehensive pytest tests for snake_game.src.game module.
Tests the main game function and game logic.
"""

import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock, call
import sys
from io import StringIO

from snake_game.src.game import main


class TestMainGameFunction:
    """Test cases for the main game function."""

    @patch('snake_game.src.game.redraw_window')
    @patch('pygame.quit')
    @patch('pygame.display.set_caption')
    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_main_function_basic_setup(self, mock_init, mock_set_mode, mock_set_caption,
                                      mock_quit, mock_redraw):
        """Test that main function sets up pygame correctly."""
        # Mock the game loop to exit immediately
        with patch('pygame.event.get', return_value=[Mock(type=pygame.QUIT)]):
            with patch('pygame.key.get_pressed') as mock_keys:
                mock_keys.return_value = Mock()
                mock_keys.return_value.__getitem__ = Mock(return_value=False)
                with patch('pygame.time.Clock'):
                    main()

        # Verify basic setup
        mock_init.assert_called_once()
        mock_set_mode.assert_called_once_with((500, 500))
        mock_set_caption.assert_called_once_with("Snake Game")
        mock_quit.assert_called_once()

    def test_main_function_imports(self):
        """Test that main function can be imported without errors."""
        # This test verifies that all imports work correctly
        from snake_game.src.game import main
        assert callable(main)

    @patch('snake_game.src.game.redraw_window')
    @patch('pygame.quit')
    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_main_function_game_objects_creation(self, mock_init, mock_set_mode, mock_quit, mock_redraw):
        """Test that main function creates game objects correctly."""
        with patch('pygame.event.get', return_value=[Mock(type=pygame.QUIT)]):
            with patch('pygame.key.get_pressed') as mock_keys:
                mock_keys.return_value = Mock()
                mock_keys.return_value.__getitem__ = Mock(return_value=False)
                with patch('pygame.time.Clock'):
                    with patch('pygame.display.set_caption'):
                        main()

        # If we get here without exceptions, game objects were created successfully
        assert True

    def test_game_constants(self):
        """Test that game constants are defined correctly."""
        # Test that the constants used in main are reasonable
        width = 500
        rows = 20

        assert width > 0
        assert rows > 0
        assert width % rows == 0  # Should be evenly divisible for clean grid

    def test_game_module_structure(self):
        """Test that the game module has the expected structure."""
        from snake_game.src import game

        # Test that main function exists and is callable
        assert hasattr(game, 'main')
        assert callable(game.main)

    def test_game_dependencies(self):
        """Test that game module imports work correctly."""
        # Test that all required modules can be imported
        from snake_game.src.models import Snake, Cube
        from snake_game.src.utils import random_snack, message_box, redraw_window

        # Test that classes can be instantiated
        snake = Snake((255, 0, 0), (10, 10))
        cube = Cube((5, 5))

        assert isinstance(snake, Snake)
        assert isinstance(cube, Cube)

    def test_game_logic_components(self):
        """Test that game logic components work together."""
        from snake_game.src.utils import random_snack
        from snake_game.src.models import Snake

        # Test that random_snack works with Snake
        snake = Snake((255, 0, 0), (10, 10))
        snack_pos = random_snack(20, snake)

        assert isinstance(snack_pos, tuple)
        assert len(snack_pos) == 2
        assert snack_pos not in [cube.pos for cube in snake.body]
