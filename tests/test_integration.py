"""
Integration tests for the snake_game package.
Tests the interaction between different modules.
"""

import pytest
import pygame
from unittest.mock import Mock, patch

from snake_game.src.models import Snake, Cube
from snake_game.src.utils import random_snack, redraw_window
from snake_game.src.game import main


class TestSnakeGameIntegration:
    """Integration tests for the complete snake game."""

    def test_snake_and_cube_interaction(self, pygame_surface):
        """Test interaction between Snake and Cube classes."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Test that snake head is a Cube
        assert isinstance(snake.head, Cube)
        
        # Test adding cubes to snake
        initial_length = len(snake.body)
        snake.add_cube()
        
        assert len(snake.body) == initial_length + 1
        assert isinstance(snake.body[-1], Cube)
        
        # Test drawing snake (which draws individual cubes)
        snake.draw(pygame_surface)  # Should not raise any errors

    def test_snake_movement_and_boundary_wrapping(self):
        """Test snake movement with boundary wrapping."""
        snake = Snake((255, 0, 0), (0, 10))
        
        # Set snake to move left (should wrap around)
        snake.head.dirnx = -1
        snake.head.dirny = 0
        
        snake.move()
        
        # Should wrap to the right side of the grid
        assert snake.head.pos[0] == snake.head.rows - 1

    def test_random_snack_with_growing_snake(self):
        """Test random_snack function with a growing snake."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Grow the snake
        for _ in range(5):
            snake.add_cube()
        
        # Generate snack position
        snack_pos = random_snack(20, snake)
        
        # Verify snack doesn't overlap with any snake segment
        snake_positions = [cube.pos for cube in snake.body]
        assert snack_pos not in snake_positions

    def test_complete_game_cycle_simulation(self, pygame_surface):
        """Test a complete game cycle simulation."""
        # Initialize game objects
        snake = Snake((255, 0, 0), (10, 10))
        snack_pos = random_snack(20, snake)
        snack = Cube(snack_pos, color=(0, 255, 0))
        
        # Simulate snake movement towards snack
        initial_length = len(snake.body)
        
        # Move snake to snack position (simulate eating)
        snake.head.pos = snack.pos
        
        # Check if snake ate snack (position collision)
        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            # Generate new snack
            new_snack_pos = random_snack(20, snake)
            snack = Cube(new_snack_pos, color=(0, 255, 0))
        
        # Verify snake grew
        assert len(snake.body) == initial_length + 1
        
        # Verify new snack is in valid position
        snake_positions = [cube.pos for cube in snake.body]
        assert snack.pos not in snake_positions

    def test_snake_input_and_movement_integration(self):
        """Test integration between input handling and movement."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Mock pygame keys for right movement
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda key: key == pygame.K_RIGHT)
        
        # Handle input
        snake.handle_input(mock_keys)
        
        # Verify direction changed
        assert snake.dirnx == 1
        assert snake.dirny == 0
        
        # Verify turn was recorded
        assert snake.head.pos in snake.turns
        
        # Move snake
        initial_pos = snake.head.pos
        snake.move()
        
        # Verify snake moved in the right direction
        assert snake.head.pos == (initial_pos[0] + 1, initial_pos[1])

    def test_collision_detection_integration(self):
        """Test collision detection with multi-segment snake."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Add segments to create potential for collision
        snake.add_cube()
        snake.add_cube()
        
        # Manually create collision by setting positions
        snake.body[0].pos = (5, 5)  # Head
        snake.body[1].pos = (5, 6)  # Body segment
        snake.body[2].pos = (5, 5)  # Tail at same position as head
        
        # Check for collision (simulate game logic)
        collision_detected = False
        for x in range(len(snake.body)):
            if snake.body[x].pos in [cube.pos for cube in snake.body[x + 1:]]:
                collision_detected = True
                break
        
        assert collision_detected

    @patch('snake_game.src.utils.message_box')
    def test_game_over_integration(self, mock_message_box):
        """Test game over scenario integration."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Create collision scenario
        snake.add_cube()
        snake.body[0].pos = (5, 5)
        snake.body[1].pos = (5, 5)  # Same position as head
        
        # Simulate game over logic
        for x in range(len(snake.body)):
            if snake.body[x].pos in [cube.pos for cube in snake.body[x + 1:]]:
                score = len(snake.body)
                # This would normally call message_box
                mock_message_box('You Lost!', f'Your Score: {score}. Play Again?')
                snake.reset((10, 10))
                break
        
        # Verify game over handling
        mock_message_box.assert_called_once()
        assert len(snake.body) == 1  # Snake reset to initial state
        assert snake.head.pos == (10, 10)

    @patch('pygame.display.update')
    def test_redraw_window_integration(self, mock_display_update, pygame_surface):
        """Test redraw_window with all game components."""
        snake = Snake((255, 0, 0), (10, 10))
        snake.add_cube()  # Multi-segment snake

        snack = Cube((15, 15), color=(0, 255, 0))

        # This should execute without errors
        redraw_window(pygame_surface, snake, snack, 500, 20)

    def test_snake_growth_and_movement_integration(self):
        """Test snake growth affecting movement behavior."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Set initial movement direction
        snake.dirnx = 1
        snake.dirny = 0
        
        # Add several segments
        for _ in range(3):
            snake.add_cube()
        
        initial_positions = [cube.pos for cube in snake.body]
        
        # Move snake
        snake.move()
        
        # Verify all segments moved
        new_positions = [cube.pos for cube in snake.body]
        assert new_positions != initial_positions
        
        # Verify head moved in correct direction
        assert snake.head.pos[0] == initial_positions[0][0] + 1

    def test_boundary_wrapping_all_directions(self):
        """Test boundary wrapping in all four directions."""
        # Test left boundary
        snake_left = Snake((255, 0, 0), (0, 10))
        snake_left.head.dirnx = -1
        snake_left.head.dirny = 0
        snake_left.move()
        assert snake_left.head.pos[0] == 19  # Wrapped to right side
        
        # Test right boundary
        snake_right = Snake((255, 0, 0), (19, 10))
        snake_right.head.dirnx = 1
        snake_right.head.dirny = 0
        snake_right.move()
        assert snake_right.head.pos[0] == 0  # Wrapped to left side
        
        # Test top boundary
        snake_top = Snake((255, 0, 0), (10, 0))
        snake_top.head.dirnx = 0
        snake_top.head.dirny = -1
        snake_top.move()
        assert snake_top.head.pos[1] == 19  # Wrapped to bottom
        
        # Test bottom boundary
        snake_bottom = Snake((255, 0, 0), (10, 19))
        snake_bottom.head.dirnx = 0
        snake_bottom.head.dirny = 1
        snake_bottom.move()
        assert snake_bottom.head.pos[1] == 0  # Wrapped to top

    def test_snake_turns_propagation(self):
        """Test that turns propagate correctly through snake body."""
        snake = Snake((255, 0, 0), (10, 10))
        
        # Add segments
        for _ in range(3):
            snake.add_cube()
        
        # Create a turn
        snake.dirnx = 1
        snake.dirny = 0
        snake.turns[(10, 10)] = [1, 0]
        
        # Move snake multiple times to see turn propagation
        for _ in range(len(snake.body)):
            snake.move()
        
        # Turn should have been processed and removed
        assert (10, 10) not in snake.turns

    @patch('random.randrange')
    def test_snack_generation_edge_cases(self, mock_randrange):
        """Test snack generation in edge cases."""
        # Create snake that fills most of a small grid
        snake = Snake((255, 0, 0), (0, 0))
        snake.body = [
            Cube((0, 0)), Cube((0, 1)), Cube((1, 0))
        ]
        
        # Mock random to return occupied position first, then free position
        mock_randrange.side_effect = [0, 0, 1, 1]  # (0,0) occupied, (1,1) free
        
        snack_pos = random_snack(2, snake)
        
        assert snack_pos == (1, 1)
        assert snack_pos not in [cube.pos for cube in snake.body]
