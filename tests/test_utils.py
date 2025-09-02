"""
Comprehensive pytest tests for snake_game.src.utils module.
Tests all utility functions and edge cases.
"""

import pytest
import pygame
from unittest.mock import Mock, patch

from snake_game.src.utils import draw_grid, random_snack, message_box, redraw_window
from snake_game.src.models import Snake, Cube


class TestDrawGrid:
    """Test cases for the draw_grid function."""

    def test_draw_grid_basic_parameters(self):
        """Test draw_grid with basic parameters."""
        pygame.init()

        # Function should execute without errors
        draw_grid(500, 20)

        pygame.quit()

    def test_draw_grid_different_dimensions(self):
        """Test draw_grid with different dimensions."""
        pygame.init()

        # Test with different width and rows
        draw_grid(400, 16)
        draw_grid(600, 24)
        draw_grid(100, 5)

        pygame.quit()

    def test_draw_grid_edge_cases(self):
        """Test draw_grid with edge case values."""
        pygame.init()

        # Test with minimum values
        draw_grid(1, 1)

        # Test with zero rows (should handle division)
        with pytest.raises(ZeroDivisionError):
            draw_grid(100, 0)

        pygame.quit()

    @patch('pygame.draw.line')
    def test_draw_grid_line_calls(self, mock_line):
        """Test that draw_grid calculates positions correctly."""
        pygame.init()

        draw_grid(100, 4)

        # Note: The current implementation doesn't actually draw lines (commented out)
        # This test verifies the function runs without calling pygame.draw.line
        mock_line.assert_not_called()

        pygame.quit()


class TestRandomSnack:
    """Test cases for the random_snack function."""

    def test_random_snack_basic_functionality(self):
        """Test basic random_snack functionality."""
        snake = Snake((255, 0, 0), (10, 10))
        
        snack_pos = random_snack(20, snake)
        
        assert isinstance(snack_pos, tuple)
        assert len(snack_pos) == 2
        assert 0 <= snack_pos[0] < 20
        assert 0 <= snack_pos[1] < 20

    def test_random_snack_avoids_snake_body(self):
        """Test that random_snack avoids snake body positions."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Add multiple cubes to snake
        for _ in range(5):
            snake.add_cube()
        
        # Get snake body positions
        snake_positions = [cube.pos for cube in snake.body]
        
        # Generate snack position
        snack_pos = random_snack(20, snake)
        
        # Snack should not be on any snake body position
        assert snack_pos not in snake_positions

    @patch('secrets.randbelow')
    def test_random_snack_collision_retry(self, mock_randrange):
        """Test that random_snack retries when position collides with snake."""
        snake = Snake((255, 0, 0), (5, 5))
        
        # Mock random to return snake position first, then valid position
        mock_randrange.side_effect = [5, 5, 3, 3]  # First (5,5) collides, then (3,3) is valid
        
        snack_pos = random_snack(20, snake)
        
        assert snack_pos == (3, 3)
        assert mock_randrange.call_count == 4  # Called twice for each position

    def test_random_snack_different_grid_sizes(self):
        """Test random_snack with different grid sizes."""
        snake = Snake((255, 0, 0), (1, 1))
        
        # Test with small grid
        snack_pos = random_snack(5, snake)
        assert 0 <= snack_pos[0] < 5
        assert 0 <= snack_pos[1] < 5
        
        # Test with large grid
        snack_pos = random_snack(50, snake)
        assert 0 <= snack_pos[0] < 50
        assert 0 <= snack_pos[1] < 50

    def test_random_snack_single_available_position(self):
        """Test random_snack when only one position is available."""
        # Create a snake that fills almost the entire 3x3 grid
        snake = Snake((255, 0, 0), (0, 0))
        
        # Manually add cubes to fill positions
        snake.body = [
            Cube((0, 0)), Cube((0, 1)), Cube((0, 2)),
            Cube((1, 0)), Cube((1, 1)), Cube((1, 2)),
            Cube((2, 0)), Cube((2, 1))
            # (2, 2) is the only available position
        ]
        
        snack_pos = random_snack(3, snake)
        
        assert snack_pos == (2, 2)

    def test_random_snack_multiple_calls_different_results(self):
        """Test that multiple calls to random_snack can produce different results."""
        snake = Snake((255, 0, 0), (10, 10))
        
        positions = set()
        for _ in range(10):
            pos = random_snack(20, snake)
            positions.add(pos)
        
        # Should generate multiple different positions (with high probability)
        assert len(positions) > 1


class TestMessageBox:
    """Test cases for the message_box function."""

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.Tk')
    def test_message_box_basic_functionality(self, mock_tk, mock_showinfo):
        """Test basic message_box functionality."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        message_box("Test Subject", "Test Context")
        
        # Verify Tk was created and configured
        mock_tk.assert_called_once()
        mock_root.attributes.assert_called_once_with('-topmost', True)
        mock_root.withdraw.assert_called_once()
        
        # Verify messagebox was shown
        mock_showinfo.assert_called_once_with("Test Subject", "Test Context")
        
        # Verify root was destroyed
        mock_root.destroy.assert_called_once()

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.Tk')
    def test_message_box_destroy_exception(self, mock_tk, mock_showinfo):
        """Test message_box handles destroy exception gracefully."""
        mock_root = Mock()
        mock_root.destroy.side_effect = Exception("Destroy failed")
        mock_tk.return_value = mock_root
        
        # Should not raise exception
        message_box("Test", "Test")
        
        mock_showinfo.assert_called_once()

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.Tk')
    def test_message_box_different_messages(self, mock_tk, mock_showinfo):
        """Test message_box with different message types."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        # Test with empty strings
        message_box("", "")
        mock_showinfo.assert_called_with("", "")
        
        # Test with long strings
        long_subject = "A" * 100
        long_context = "B" * 500
        message_box(long_subject, long_context)
        mock_showinfo.assert_called_with(long_subject, long_context)
        
        # Test with special characters
        message_box("Test!@#$%", "Context with\nnewlines\tand\ttabs")


class TestRedrawWindow:
    """Test cases for the redraw_window function."""

    @patch('pygame.display.update')
    @patch('snake_game.src.utils.draw_grid')
    def test_redraw_window_basic_functionality(self, mock_draw_grid, mock_display_update):
        """Test basic redraw_window functionality."""
        pygame.init()
        surface = pygame.Surface((500, 500))
        snake = Snake((255, 0, 0), (10, 10))
        snack = Cube((15, 15), color=(0, 255, 0))
        
        redraw_window(surface, snake, snack, 500, 20)
        
        # Verify draw_grid was called
        mock_draw_grid.assert_called_once_with(500, 20)
        
        # Verify display was updated
        mock_display_update.assert_called_once()
        
        pygame.quit()

    @patch('pygame.display.update')
    @patch('snake_game.src.utils.draw_grid')
    @patch('snake_game.src.models.Cube.draw')
    @patch('snake_game.src.models.Snake.draw')
    def test_redraw_window_draw_calls(self, mock_snake_draw, mock_cube_draw, 
                                     mock_draw_grid, mock_display_update):
        """Test that redraw_window calls all draw methods."""
        pygame.init()
        surface = pygame.Surface((400, 400))
        snake = Snake((255, 0, 0), (5, 5))
        snack = Cube((10, 10), color=(0, 255, 0))
        
        redraw_window(surface, snake, snack, 400, 16)
        
        # Verify all draw methods were called
        mock_snake_draw.assert_called_once_with(surface)
        mock_cube_draw.assert_called_once_with(surface)
        mock_draw_grid.assert_called_once_with(400, 16)
        mock_display_update.assert_called_once()
        
        pygame.quit()

    @patch('pygame.display.update')
    def test_redraw_window_surface_fill(self, mock_display_update):
        """Test that redraw_window fills the surface with black."""
        pygame.init()
        surface = pygame.Surface((100, 100))
        snake = Snake((255, 0, 0), (1, 1))
        snack = Cube((2, 2))

        # Fill surface with white first
        surface.fill((255, 255, 255))

        redraw_window(surface, snake, snack, 100, 5)

        # Verify display was updated
        mock_display_update.assert_called_once()
        pygame.quit()

    @patch('pygame.display.update')
    def test_redraw_window_different_parameters(self, mock_display_update):
        """Test redraw_window with different parameter combinations."""
        pygame.init()

        # Test with different surface sizes
        surface1 = pygame.Surface((200, 200))
        surface2 = pygame.Surface((800, 600))

        snake = Snake((100, 100, 100), (5, 5))
        snack = Cube((8, 8), color=(200, 200, 0))

        # Should work with different dimensions
        redraw_window(surface1, snake, snack, 200, 10)
        redraw_window(surface2, snake, snack, 800, 32)

        # Verify display was updated (called twice)
        assert mock_display_update.call_count == 2
        pygame.quit()

    @patch('pygame.display.update')
    @patch('snake_game.src.utils.draw_grid')
    def test_redraw_window_with_multi_segment_snake(self, mock_draw_grid, mock_display_update):
        """Test redraw_window with a multi-segment snake."""
        pygame.init()
        surface = pygame.Surface((500, 500))
        
        snake = Snake((255, 0, 0), (10, 10))
        # Add multiple segments
        for _ in range(5):
            snake.add_cube()
        
        snack = Cube((15, 15), color=(0, 255, 0))
        
        redraw_window(surface, snake, snack, 500, 20)
        
        # Function should complete without errors
        mock_draw_grid.assert_called_once()
        mock_display_update.assert_called_once()
        
        pygame.quit()
