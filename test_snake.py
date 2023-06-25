import unittest
from unittest.mock import patch
import curses
import random
from snake import SnakeGame

class SnakeGameTestCase(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame()

    def tearDown(self):
        curses.endwin()

    def test_handle_input(self):
        with patch("snake_game.SnakeGame.window.getch", return_value=curses.KEY_DOWN):
            self.game.handle_input()
            self.assertEqual(self.game.direction, curses.KEY_DOWN)

        with patch("snake_game.SnakeGame.window.getch", return_value=curses.KEY_LEFT):
            self.game.handle_input()
            self.assertEqual(self.game.direction, curses.KEY_LEFT)

    def test_get_new_head(self):
        self.game.direction = curses.KEY_DOWN
        self.assertEqual(self.game.get_new_head(), [self.game.snake[0][0] + 1, self.game.snake[0][1]])

        self.game.direction = curses.KEY_UP
        self.assertEqual(self.game.get_new_head(), [self.game.snake[0][0] - 1, self.game.snake[0][1]])

        self.game.direction = curses.KEY_LEFT
        self.assertEqual(self.game.get_new_head(), [self.game.snake[0][0], self.game.snake[0][1] - 1])

        self.game.direction = curses.KEY_RIGHT
        self.assertEqual(self.game.get_new_head(), [self.game.snake[0][0], self.game.snake[0][1] + 1])

    def test_is_collision(self):
        self.assertFalse(self.game.is_collision())

        self.game.snake[0] = [0, 0]
        self.assertTrue(self.game.is_collision())

        self.game.snake[0] = [self.game.screen_height - 1, self.game.screen_width - 1]
        self.assertTrue(self.game.is_collision())

        self.game.snake.insert(1, [self.game.snake[0][0], self.game.snake[0][1] + 1])
        self.assertTrue(self.game.is_collision())

    def test_update_head(self):
        new_head = [self.game.snake[0][0] + 1, self.game.snake[0][1]]
        self.game.update_head(new_head)
        self.assertEqual(self.game.snake[0], new_head)

    def test_consume_food(self):
        original_food = self.game.food
        self.game.consume_food()
        self.assertNotEqual(self.game.food, original_food)

    def test_place_food(self):
        with patch("snake_game.SnakeGame.window.addch") as mock_addch:
            self.game.place_food()
            mock_addch.assert_called_once()

    def test_move_snake(self):
        with patch("snake_game.SnakeGame.window.addch") as mock_addch:
            self.game.move_snake()
            mock_addch.assert_called()

    def test_is_opposite_direction(self):
        self.assertTrue(self.game.is_opposite_direction(curses.KEY_DOWN, curses.KEY_UP))
        self.assertTrue(self.game.is_opposite_direction(curses.KEY_UP, curses.KEY_DOWN))
        self.assertTrue(self.game.is_opposite_direction(curses.KEY_LEFT, curses.KEY_RIGHT))
        self.assertTrue(self.game.is_opposite_direction(curses.KEY_RIGHT, curses.KEY_LEFT))
        self.assertFalse(self.game.is_opposite_direction(curses.KEY_DOWN, curses.KEY_DOWN))
        self.assertFalse(self.game.is_opposite_direction(curses.KEY_UP, curses.KEY_UP))
        self.assertFalse(self.game.is_opposite_direction(curses.KEY_LEFT, curses.KEY_LEFT))
        self.assertFalse(self.game.is_opposite_direction(curses.KEY_RIGHT, curses.KEY_RIGHT))

if __name__ == '__main__':
    unittest.main()