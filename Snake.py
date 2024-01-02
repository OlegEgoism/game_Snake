import pygame
from random import randrange

game_width, game_height = 400, 600  # Ширина, Высота экрана
size = 20  # Размер
x, y = randrange(size, game_width - size, size), randrange(size, game_height - size, size)  # Начальное случайное положение змеи
apple = randrange(size, game_width - size, size), randrange(size, game_height - size, size)  # Начальное случайное положение яблок
length = 1  # Длина змейки
snake = [(x, y)]  # Координаты змейки
dx, dy = 0, 0  # Направление движения
fps = 60  # Кадры и скорость
speed_count, snake_speed = 0, 20  # Скорость змейки от и до
dirs = {'W': True, 'S': True, 'A': True, 'D': True}  # Назначение клавиш
score = 0  # Очки в начале игры
pygame.init()  # Модуль
surface = pygame.display.set_mode([game_width, game_height])  # Окно экрана
clock = pygame.time.Clock()  # Скорость змейки регулятор
font_score = pygame.font.SysFont('Times New Roman', 25, bold=True)  # Надпись Очки размер текста
img = pygame.image.load('Fon.jpg').convert()  # Изображение фона
pygame.mixer.init()
sound = pygame.mixer.Sound("Point.wav")  # Музыка игры
pygame.mixer.music.load('Game.wav')  # Звук змейки
game_over_sound_played = False
pygame.mixer.init()
pygame.mixer.music.play(-1)


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


while True:
    surface.blit(img, (0, 0))
    for i, j in snake:
        # Рисуем границу вокруг каждого сегмента змеи
        pygame.draw.rect(surface, pygame.Color('black'), (i, j, size, size))  # Обводка
        pygame.draw.rect(surface, pygame.Color('green'), (i + 2, j + 2, size - 4, size - 4))
    pygame.draw.circle(surface, pygame.Color('yellow'), (apple[0] + size // 2, apple[1] + size // 2), size // 2)  # Цвет кубика

    render_score = font_score.render(f'Очки: {score}', 0, pygame.Color('royalblue'))  # Надпись Очки цвет
    surface.blit(render_score, (6, 2))  # Надпись очки расположение
    speed_count += 1  # Движение змейки
    if not speed_count % snake_speed:
        x += dx * size
        y += dy * size
        snake.append((x, y))
        snake = snake[-length:]

    if snake[-1] == apple:
        apple = randrange(size, game_width - size, size), randrange(size, game_height - size, size)  # Нахождение обьекта
        length += 1
        score += 1
        snake_speed -= 1
        snake_speed = max(snake_speed, 4)
        sound.play()
    if x < 0 or x > game_width - size or y < 0 or y > game_height - size or len(snake) != len(
            set(snake)):  # Границы игры
        while True:
            render_end = pygame.image.load('End.jpg').convert()  # 280x160
            surface.blit(render_end, (game_width / 2 - 140, game_height / 3))  # Картинка игре конец
            pygame.display.flip()
            close_game()

    pygame.display.flip()  # Управление клавишами
    clock.tick(fps)
    close_game()
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        if dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
    elif key[pygame.K_s]:
        if dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
    elif key[pygame.K_a]:
        if dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
    elif key[pygame.K_d]:
        if dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True, }
    elif key[pygame.K_UP]:
        if dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True}
    elif key[pygame.K_DOWN]:
        if dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True}
    elif key[pygame.K_LEFT]:
        if dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False}
    elif key[pygame.K_RIGHT]:
        if dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True}
