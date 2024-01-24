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
SPEED = 10

# Центральные координаты игрового поля:
BOARD_CENTRE = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых обЪектов."""

    def __init__(self, obj_position=BOARD_CENTRE,
                 body_color=APPLE_COLOR) -> None:
        self.position = obj_position
        self.body_color = body_color

    def draw(self, surface: pygame.surface.Surface) -> None:
        """Метод, предназначенный для переопределения в дочерних классах."""


class Snake(GameObject):
    """Класс, описывающий змейку и ее поведение."""

    def __init__(self) -> None:
        super().__init__(BOARD_CENTRE, SNAKE_COLOR)
        self.length = 1
        self.positions: list = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
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
        self.positions.insert(0, new_head)

    def draw(self, surface) -> None:
        """Метод отрисовывает змейку на экране, затирая след."""
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

    def get_head_position(self) -> tuple[int, int]:
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self, surface: pygame.surface.Surface) -> None:
        """Метод сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        surface.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.position = BOARD_CENTRE
        self.positions.clear()
        self.positions.append(self.position)
        self.last = None
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, snake=None) -> None:
        if not snake:
            snake = Snake()
        self.snake = snake
        position = self.randomize_position()
        super().__init__(position, APPLE_COLOR)

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
    direct_keys = {(pygame.K_UP, LEFT): UP, (pygame.K_UP, RIGHT): UP,
                   (pygame.K_DOWN, LEFT): DOWN, (pygame.K_DOWN, RIGHT): DOWN,
                   (pygame.K_LEFT, UP): LEFT, (pygame.K_LEFT, DOWN): LEFT,
                   (pygame.K_RIGHT, UP): RIGHT, (pygame.K_RIGHT, DOWN): RIGHT}

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN and (
                event.key, game_object.direction) in direct_keys:
            game_object.next_direction = direct_keys[(
                event.key, game_object.direction)]


def main():
    """Основная функция запуска игры."""
    # Создаем экземпляры классов.
    snake = Snake()
    apple = Apple(snake)

    while True:
        clock.tick(SPEED)

        if not handle_keys(snake):
            pygame.quit()
            return

        snake.update_direction()

        snake.move()

        head = snake.get_head_position()

        if head in snake.positions[1:]:
            snake.reset(screen)
            continue

        if head == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        else:
            snake.last = snake.positions.pop()

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
