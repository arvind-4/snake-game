"""
Comprehensive pytest tests for snake_game.src.models module.
Tests all classes, methods, and edge cases.
"""

import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock
from typing import Tuple, List

from snake_game.src.models import Cube, Snake


class TestCube:
    """Test cases for the Cube class."""

    def test_cube_initialization_default_values(self):
        """Test Cube initialization with default values."""
        cube = Cube((5, 10))
        
        assert cube.pos == (5, 10)
        assert cube.dirnx == 1
        assert cube.dirny == 0
        assert cube.color == (255, 0, 0)

    def test_cube_initialization_custom_values(self):
        """Test Cube initialization with custom values."""
        cube = Cube((3, 7), dirnx=-1, dirny=1, color=(0, 255, 0))
        
        assert cube.pos == (3, 7)
        assert cube.dirnx == -1
        assert cube.dirny == 1
        assert cube.color == (0, 255, 0)

    def test_cube_class_variables(self):
        """Test Cube class variables."""
        assert Cube.rows == 20
        assert Cube.w == 500

    def test_cube_move_positive_direction(self):
        """Test cube movement in positive direction."""
        cube = Cube((5, 5))
        cube.move(1, 1)
        
        assert cube.pos == (6, 6)
        assert cube.dirnx == 1
        assert cube.dirny == 1

    def test_cube_move_negative_direction(self):
        """Test cube movement in negative direction."""
        cube = Cube((10, 10))
        cube.move(-1, -1)
        
        assert cube.pos == (9, 9)
        assert cube.dirnx == -1
        assert cube.dirny == -1

    def test_cube_move_zero_direction(self):
        """Test cube movement with zero direction."""
        cube = Cube((5, 5))
        cube.move(0, 0)
        
        assert cube.pos == (5, 5)
        assert cube.dirnx == 0
        assert cube.dirny == 0

    def test_cube_multiple_moves(self):
        """Test multiple consecutive moves."""
        cube = Cube((0, 0))
        
        cube.move(1, 0)
        assert cube.pos == (1, 0)
        
        cube.move(0, 1)
        assert cube.pos == (1, 1)
        
        cube.move(-1, 0)
        assert cube.pos == (0, 1)

    @patch('pygame.draw.rect')
    def test_cube_draw_without_eyes(self, mock_rect):
        """Test cube drawing without eyes."""
        pygame.init()
        surface = pygame.Surface((500, 500))
        cube = Cube((2, 3), color=(100, 150, 200))
        
        cube.draw(surface, eyes=False)
        
        # Verify pygame.draw.rect was called with correct parameters
        expected_dis = cube.w // cube.rows  # 25
        expected_rect = (2 * expected_dis + 1, 3 * expected_dis + 1, expected_dis - 2, expected_dis - 2)
        mock_rect.assert_called_once_with(surface, (100, 150, 200), expected_rect)
        
        pygame.quit()

    @patch('pygame.draw.circle')
    @patch('pygame.draw.rect')
    def test_cube_draw_with_eyes(self, mock_rect, mock_circle):
        """Test cube drawing with eyes."""
        pygame.init()
        surface = pygame.Surface((500, 500))
        cube = Cube((1, 1), color=(255, 0, 0))
        
        cube.draw(surface, eyes=True)
        
        # Verify rect was drawn
        mock_rect.assert_called_once()
        
        # Verify two circles (eyes) were drawn
        assert mock_circle.call_count == 2
        
        pygame.quit()

    def test_cube_position_boundary_values(self):
        """Test cube with boundary position values."""
        # Test with zero coordinates
        cube1 = Cube((0, 0))
        assert cube1.pos == (0, 0)
        
        # Test with maximum coordinates
        cube2 = Cube((19, 19))
        assert cube2.pos == (19, 19)
        
        # Test with negative coordinates (edge case)
        cube3 = Cube((-1, -1))
        assert cube3.pos == (-1, -1)


class TestSnake:
    """Test cases for the Snake class."""

    def test_snake_initialization(self):
        """Test Snake initialization."""
        snake = Snake((255, 0, 0), (10, 10))
        
        assert snake.color == (255, 0, 0)
        assert snake.head.pos == (10, 10)
        assert len(snake.body) == 1
        assert snake.body[0] == snake.head
        assert snake.dirnx == 0
        assert snake.dirny == 1
        assert isinstance(snake.turns, dict)
        assert len(snake.turns) == 0

    def test_snake_head_properties(self):
        """Test snake head properties."""
        snake = Snake((0, 255, 0), (5, 7))
        
        assert isinstance(snake.head, Cube)
        assert snake.head.pos == (5, 7)
        assert snake.head.color == (255, 0, 0)  # Default cube color

    def test_snake_handle_input_left(self):
        """Test snake input handling for left direction."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Mock pygame keys
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda key: key == pygame.K_LEFT)
        
        snake.handle_input(mock_keys)
        
        assert snake.dirnx == -1
        assert snake.dirny == 0
        assert snake.head.pos in snake.turns
        assert snake.turns[snake.head.pos] == [-1, 0]

    def test_snake_handle_input_right(self):
        """Test snake input handling for right direction."""
        snake = Snake((255, 0, 0), (10, 10))
        
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda key: key == pygame.K_RIGHT)
        
        snake.handle_input(mock_keys)
        
        assert snake.dirnx == 1
        assert snake.dirny == 0

    def test_snake_handle_input_up(self):
        """Test snake input handling for up direction."""
        snake = Snake((255, 0, 0), (10, 10))
        # Change initial direction so UP movement is allowed
        snake.dirny = 0  # Not moving down, so UP is allowed

        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda key: key == pygame.K_UP)

        snake.handle_input(mock_keys)

        assert snake.dirnx == 0
        assert snake.dirny == -1

    def test_snake_handle_input_down(self):
        """Test snake input handling for down direction."""
        snake = Snake((255, 0, 0), (10, 10))
        snake.dirny = 0  # Change initial direction to test down movement
        
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda key: key == pygame.K_DOWN)
        
        snake.handle_input(mock_keys)
        
        assert snake.dirnx == 0
        assert snake.dirny == 1

    def test_snake_prevent_backwards_movement(self):
        """Test that snake cannot move backwards."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Set snake moving right
        snake.dirnx = 1
        snake.dirny = 0
        
        # Try to move left (backwards)
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda key: key == pygame.K_LEFT)
        
        snake.handle_input(mock_keys)
        
        # Should still be moving right
        assert snake.dirnx == 1
        assert snake.dirny == 0

    def test_snake_move_simple(self):
        """Test basic snake movement."""
        snake = Snake((255, 0, 0), (10, 10))
        snake.dirnx = 1
        snake.dirny = 0
        
        initial_pos = snake.head.pos
        snake.move()
        
        # Head should move in the direction
        assert snake.head.pos == (initial_pos[0] + 1, initial_pos[1])

    def test_snake_move_with_turns(self):
        """Test snake movement with turns."""
        snake = Snake((255, 0, 0), (10, 10))

        # Add a turn at the head position
        snake.turns[(10, 10)] = [1, 0]

        snake.move()

        # Turn should be processed and removed
        assert (10, 10) not in snake.turns

    def test_snake_boundary_wrapping_left(self):
        """Test snake wrapping around left boundary."""
        snake = Snake((255, 0, 0), (0, 10))
        snake.head.dirnx = -1
        snake.head.dirny = 0

        snake.move()

        # Should wrap to right side
        assert snake.head.pos[0] == snake.head.rows - 1

    def test_snake_boundary_wrapping_right(self):
        """Test snake wrapping around right boundary."""
        snake = Snake((255, 0, 0), (19, 10))
        snake.head.dirnx = 1
        snake.head.dirny = 0

        snake.move()

        # Should wrap to left side
        assert snake.head.pos[0] == 0

    def test_snake_boundary_wrapping_top(self):
        """Test snake wrapping around top boundary."""
        snake = Snake((255, 0, 0), (10, 0))
        snake.head.dirnx = 0
        snake.head.dirny = -1

        snake.move()

        # Should wrap to bottom
        assert snake.head.pos[1] == snake.head.rows - 1

    def test_snake_boundary_wrapping_bottom(self):
        """Test snake wrapping around bottom boundary."""
        snake = Snake((255, 0, 0), (10, 19))
        snake.head.dirnx = 0
        snake.head.dirny = 1

        snake.move()

        # Should wrap to top
        assert snake.head.pos[1] == 0

    def test_snake_reset(self):
        """Test snake reset functionality."""
        snake = Snake((255, 0, 0), (10, 10))

        # Add some cubes and turns
        snake.add_cube()
        snake.add_cube()
        snake.turns[(5, 5)] = [1, 0]
        snake.dirnx = -1
        snake.dirny = -1

        # Reset snake
        snake.reset((15, 15))

        assert snake.head.pos == (15, 15)
        assert len(snake.body) == 1
        assert snake.body[0] == snake.head
        assert len(snake.turns) == 0
        assert snake.dirnx == 0
        assert snake.dirny == 1

    def test_snake_add_cube_moving_right(self):
        """Test adding cube when snake is moving right."""
        snake = Snake((255, 0, 0), (10, 10))
        snake.body[0].dirnx = 1
        snake.body[0].dirny = 0

        initial_length = len(snake.body)
        snake.add_cube()

        assert len(snake.body) == initial_length + 1
        new_cube = snake.body[-1]
        assert new_cube.pos == (9, 10)  # One position to the left
        assert new_cube.dirnx == 1
        assert new_cube.dirny == 0

    def test_snake_add_cube_moving_left(self):
        """Test adding cube when snake is moving left."""
        snake = Snake((255, 0, 0), (10, 10))
        snake.body[0].dirnx = -1
        snake.body[0].dirny = 0

        snake.add_cube()

        new_cube = snake.body[-1]
        assert new_cube.pos == (11, 10)  # One position to the right

    def test_snake_add_cube_moving_up(self):
        """Test adding cube when snake is moving up."""
        snake = Snake((255, 0, 0), (10, 10))
        snake.body[0].dirnx = 0
        snake.body[0].dirny = -1

        snake.add_cube()

        new_cube = snake.body[-1]
        assert new_cube.pos == (10, 11)  # One position down

    def test_snake_add_cube_moving_down(self):
        """Test adding cube when snake is moving down."""
        snake = Snake((255, 0, 0), (10, 10))
        snake.body[0].dirnx = 0
        snake.body[0].dirny = 1

        snake.add_cube()

        new_cube = snake.body[-1]
        assert new_cube.pos == (10, 9)  # One position up

    @patch('snake_game.src.models.Cube.draw')
    def test_snake_draw(self, mock_cube_draw):
        """Test snake drawing functionality."""
        pygame.init()
        surface = pygame.Surface((500, 500))

        snake = Snake((255, 0, 0), (10, 10))
        snake.add_cube()
        snake.add_cube()

        snake.draw(surface)

        # Should call draw for each cube in body
        assert mock_cube_draw.call_count == len(snake.body)

        # First call should have eyes=True (head)
        first_call_args = mock_cube_draw.call_args_list[0]
        assert first_call_args[0][1] == True  # eyes parameter

        # Other calls should have eyes=False
        for call_args in mock_cube_draw.call_args_list[1:]:
            assert len(call_args[0]) == 1  # Only surface parameter, eyes defaults to False

        pygame.quit()

    def test_snake_multiple_cubes(self):
        """Test snake with multiple cubes."""
        snake = Snake((255, 0, 0), (10, 10))

        # Add multiple cubes
        for _ in range(5):
            snake.add_cube()

        assert len(snake.body) == 6  # Original head + 5 added cubes

        # All cubes should be Cube instances
        for cube in snake.body:
            assert isinstance(cube, Cube)

    def test_snake_no_input_pressed(self):
        """Test snake input handling when no keys are pressed."""
        snake = Snake((255, 0, 0), (10, 10))
        original_dirnx = snake.dirnx
        original_dirny = snake.dirny

        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(return_value=False)

        snake.handle_input(mock_keys)

        # Direction should remain unchanged
        assert snake.dirnx == original_dirnx
        assert snake.dirny == original_dirny
