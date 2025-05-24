import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг")

# Часы для контроля FPS
clock = pygame.time.Clock()


# Класс ракетки
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 7

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


# Класс мяча
class Ball:
    def __init__(self):
        self.initial_speed = 1.75  # Определяем initial_speed перед reset()
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                                HEIGHT // 2 - BALL_SIZE // 2,
                                BALL_SIZE, BALL_SIZE)
        # При сбросе возвращаем начальную скорость (без ускорения)
        self.speed_x = self.initial_speed * random.choice((1, -1))
        self.speed_y = self.initial_speed * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верхней и нижней границы
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

        # Проверка выхода за границы (проигрыш)
        if self.rect.left <= 0:
            return "right"
        if self.rect.right >= WIDTH:
            return "left"

        return None

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def collide_with_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            # Изменяем направление и немного увеличиваем скорость
            self.speed_x *= -1.1
            self.speed_y *= 1.1


# Создание объектов
player_left = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
player_right = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Счет
score_left = 0
score_right = 0
font = pygame.font.Font(None, 36)

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение ракеток
    player_left.move(pygame.K_w, pygame.K_s)
    player_right.move(pygame.K_UP, pygame.K_DOWN)

    # Движение мяча и проверка коллизий
    result = ball.move()
    if result == "left":
        score_right += 1
        ball.reset()
    elif result == "right":
        score_left += 1
        ball.reset()

    ball.collide_with_paddle(player_left)
    ball.collide_with_paddle(player_right)

    # Отрисовка
    screen.fill(BLACK)

    # Рисуем разделительную линию
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Рисуем объекты
    player_left.draw()
    player_right.draw()
    ball.draw()

    # Отображаем счет
    score_text = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()