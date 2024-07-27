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
font_button_text = pygame.font.SysFont('Times New Roman', 20, bold=True)  # Шрифт для кнопок
img = pygame.image.load('Fon.jpg').convert()  # Изображение фона
pygame.mixer.init()
sound = pygame.mixer.Sound("Point.wav")  # Музыка игры
pygame.mixer.music.load('Game.wav')  # Звук змейки
game_over_sound_played = False
pygame.mixer.music.play(-1)

# Установить начальную громкость
volume = 0.3
pygame.mixer.music.set_volume(volume)

def increase_volume():
    global volume
    if volume < 1.0:
        volume += 0.01
        pygame.mixer.music.set_volume(volume)
        sound.set_volume(volume)

def decrease_volume():
    global volume
    if volume > 0.0:
        volume -= 0.01
        pygame.mixer.music.set_volume(volume)
        sound.set_volume(volume)

def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def draw_transparent_button(surface, text, rect, color, alpha):
    button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)  # Создаем поверхность с поддержкой альфа-канала
    button_surface.fill((*color[:3], alpha))  # Заполняем поверхность цветом с прозрачностью
    render_text = font_button_text.render(text, True, pygame.Color('white'))
    button_surface.blit(render_text, render_text.get_rect(center=(rect.width // 2, rect.height // 2)))
    surface.blit(button_surface, rect.topleft)

def draw_volume_label(surface, text, rect, color):
    label_surface = pygame.Surface((rect.width, 30), pygame.SRCALPHA)  # Создаем поверхность для текста
    label_surface.fill((0, 0, 0, 0))  # Прозрачный фон
    render_text = font_button_text.render(text, True, color)
    label_surface.blit(render_text, (0, 0))
    surface.blit(label_surface, rect.topleft)

button_plus = pygame.Rect(game_width - 34, game_height - 600, 30, 30)
button_minus = pygame.Rect(game_width - 70, game_height - 600, 30, 30)
label_volume = pygame.Rect(game_width - 170, game_height - 600, 100, 30)

while True:
    surface.blit(img, (0, 0))
    for i, j in snake:
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
    if x < 0 or x > game_width - size or y < 0 or y > game_height - size or len(snake) != len(set(snake)):  # Границы игры
        while True:
            render_end = pygame.image.load('End.jpg').convert()  # 280x160
            surface.blit(render_end, (game_width / 2 - 140, game_height / 3))  # Картинка игре конец
            pygame.display.flip()
            close_game()

    # Отрисовка прозрачных кнопок регулировки громкости
    draw_transparent_button(surface, '+', button_plus, (0, 0, 10), 66)
    draw_transparent_button(surface, '-', button_minus, (0, 0, 10), 66)

    # Отрисовка текста "Громкость" напротив кнопок
    draw_volume_label(surface, 'Громкость', label_volume, pygame.Color('white'))

    pygame.display.flip()  # Управление клавишами
    clock.tick(fps)
    close_game()

    key = pygame.key.get_pressed()
    if key[pygame.K_w] and dirs['W']:
        dx, dy = 0, -1
        dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
    elif key[pygame.K_s] and dirs['S']:
        dx, dy = 0, 1
        dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
    elif key[pygame.K_a] and dirs['A']:
        dx, dy = -1, 0
        dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
    elif key[pygame.K_d] and dirs['D']:
        dx, dy = 1, 0
        dirs = {'W': True, 'S': True, 'A': False, 'D': True, }
    elif key[pygame.K_UP] and dirs['W']:
        dx, dy = 0, -1
        dirs = {'W': True, 'S': False, 'A': True, 'D': True}
    elif key[pygame.K_DOWN] and dirs['S']:
        dx, dy = 0, 1
        dirs = {'W': False, 'S': True, 'A': True, 'D': True}
    elif key[pygame.K_LEFT] and dirs['A']:
        dx, dy = -1, 0
        dirs = {'W': True, 'S': True, 'A': True, 'D': False}
    elif key[pygame.K_RIGHT] and dirs['D']:
        dx, dy = 1, 0
        dirs = {'W': True, 'S': True, 'A': False, 'D': True}

    # Обработка регулировки громкости с помощью кнопок
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if button_plus.collidepoint(mouse_pos) and mouse_click[0]:
        increase_volume()
    elif button_minus.collidepoint(mouse_pos) and mouse_click[0]:
        decrease_volume()

    # Обработка регулировки громкости с помощью клавиш
    if key[pygame.K_PLUS] or key[pygame.K_EQUALS]:  # Клавиша "+" или "="
        increase_volume()
    elif key[pygame.K_MINUS]:  # Клавиша "-"
        decrease_volume()
