from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых обЪектов."""

    board_centre = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def __init__(self) -> None:
        self.position = self.board_centre
        self.body_color = None

    def draw(self, surface: pygame.surface.Surface) -> None:
        """Метод, предназначенный для переопределения в дочерних классах."""
        pass


class Snake(GameObject):
    """Класс, описывающий змейку и ее поведение."""

    length = 1
    positions: list[tuple[int, int]] = []
    direction = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self) -> None:
        super().__init__()
        self.positions.clear()
        self.positions.append(self.position)
        self.body_color = Snake.body_color
        self.last = None
        self.flag = False

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_obj) -> None:
        """Метод обновляет позицию змейки и
        реагирует на столкновение с яблоком или с собой.
        """
        head = self.get_head_position()

        # Вычисление координат для головы змеи.
        x = head[0] + self.direction[0] * GRID_SIZE
        y = head[1] + self.direction[1] * GRID_SIZE
        new_x = x if 0 <= x < SCREEN_WIDTH else SCREEN_WIDTH - abs(x)
        new_y = y if 0 <= y < SCREEN_HEIGHT else SCREEN_HEIGHT - abs(y)

        new_head = (new_x, new_y)

        # Добавление координат головы и удаление хвоста,
        # если яблоко не съедено.
        if new_head in self.positions:
            self.flag = True
        else:
            self.positions.insert(0, new_head)

            if new_head == apple_obj.position:
                self.length += 1
                apple_obj.position = apple_obj.randomize_position()
            else:
                self.last = self.positions.pop()

    def draw(self, surface) -> None:
        """Метод отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    @classmethod
    def get_head_position(cls) -> tuple[int, int]:
        """Метод возвращает позицию головы змейки."""
        return cls.positions[0]

    def reset(self, surface: pygame.surface.Surface) -> None:
        """Метод сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        surface.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions.clear()
        self.positions.append(self.board_centre)
        self.last = None
        self.flag = False
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, snake=Snake()) -> None:
        super().__init__()
        self.snake = snake
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self) -> tuple[int, int]:
        """Устанавливает случайное положение яблока на игровом поле."""
        position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

        while position in self.snake.positions:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

        return position

    def draw(self, surface: pygame.surface.Surface) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object: Snake):
    """Функция обработки действий пользователя: нажатие клавиш,
    изменяя направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция запуска игры."""
    # Создаем экземпляры классов.
    snake = Snake()
    apple = Apple(snake)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)

        apple.draw(screen)
        snake.draw(screen)

        if snake.flag:
            snake.reset(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
