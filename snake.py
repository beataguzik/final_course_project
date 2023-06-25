import curses
import time
import random

class SnakeGame:
    def __init__(self):
        curses.initscr()
        curses.curs_set(0)
        self.window = curses.newwin(0, 0)
        self.window.keypad(1)
        self.window.timeout(100)

        self.screen_height, self.screen_width = self.window.getmaxyx()
        self.window.border(0)

        self.snake_x = self.screen_width // 4
        self.snake_y = self.screen_height // 2
        self.snake = [
            [self.snake_y, self.snake_x],
            [self.snake_y, self.snake_x - 1],
            [self.snake_y, self.snake_x - 2]
        ]

        self.food = [self.screen_height // 2, self.screen_width // 2]
        self.place_food()

        self.direction = curses.KEY_RIGHT
        self.prev_direction = self.direction

        self.score = 0
        self.is_game_over = False

    def play(self):
        self.is_game_over = False
        self.score = 0

        while not self.is_game_over:
            self.handle_input()

            if self.is_collision():
                self.game_over()
                break

            new_head = self.get_new_head()
            self.update_head(new_head)

            if self.snake[0] == self.food:
                self.consume_food()
                self.score += 1
                self.update_score()
            else:
                self.move_snake()

            self.window.refresh()

    def handle_input(self):
        next_key = self.window.getch()
        self.direction = self.direction if next_key == -1 else next_key

        if self.is_opposite_direction(self.direction, self.prev_direction):
            self.direction = self.prev_direction

        self.prev_direction = self.direction

    def get_new_head(self):
        new_head = [self.snake[0][0], self.snake[0][1]]

        if self.direction == curses.KEY_DOWN:
            new_head[0] += 1
        elif self.direction == curses.KEY_UP:
            new_head[0] -= 1
        elif self.direction == curses.KEY_LEFT:
            new_head[1] -= 1
        elif self.direction == curses.KEY_RIGHT:
            new_head[1] += 1

        return new_head

    def is_collision(self):
        head = self.snake[0]
        return (
            head[0] in [0, self.screen_height - 1] or
            head[1] in [0, self.screen_width - 1] or
            head in self.snake[1:]
        )

    def update_head(self, new_head):
        self.snake.insert(0, new_head)

    def consume_food(self):
        self.place_food()

    def place_food(self):
        self.food = None
        while self.food is None:
            new_food = [
                random.randint(1, self.screen_height - 2),
                random.randint(1, self.screen_width - 2)
            ]
            self.food = new_food if new_food not in self.snake else None
        try:
            self.window.addch(self.food[0], self.food[1], curses.ACS_LANTERN)
        except curses.error:
            pass

    def move_snake(self):
        tail = self.snake.pop()
        try:
            self.window.addch(tail[0], tail[1], ' ')
        except curses.error:
            pass
        try:
            self.window.addch(self.snake[0][0], self.snake[0][1], curses.ACS_CKBOARD)
        except curses.error:
            pass

    def is_opposite_direction(self, dir1, dir2):
        return (
            (dir1 == curses.KEY_DOWN and dir2 == curses.KEY_UP) or
            (dir1 == curses.KEY_UP and dir2 == curses.KEY_DOWN) or
            (dir1 == curses.KEY_LEFT and dir2 == curses.KEY_RIGHT) or
            (dir1 == curses.KEY_RIGHT and dir2 == curses.KEY_LEFT)
        )

    def game_over(self):
        self.is_game_over = True
        curses.endwin()
        print("Game Over. Your score:", self.score)
        self.ask_play_again()

    def update_score(self):
        score_text = "Score: {}".format(self.score)
        score_x = (self.screen_width - len(score_text)) // 2
        try:
            self.window.addstr(0, score_x, score_text)
        except curses.error:
            pass

    def ask_play_again(self):
        print("Do you want to play again? (y/n)")
        choice = input().lower().strip()
        if choice == 'y':
            self.reset_game()
            self.play()
        else:
            print("Thank you for playing!")

    def reset_game(self):
        self.window.clear()
        self.window.border(0)
        self.snake = [
            [self.snake_y, self.snake_x],
            [self.snake_y, self.snake_x - 1],
            [self.snake_y, self.snake_x - 2]
        ]
        self.direction = curses.KEY_RIGHT
        self.prev_direction = self.direction
        self.place_food()
        self.is_game_over = False
        self.score = 0

def main():
    try:
        game = SnakeGame()
        game.play()
    except KeyboardInterrupt:
        curses.endwin()
        print("Game aborted.")

if __name__ == '__main__':
    main()