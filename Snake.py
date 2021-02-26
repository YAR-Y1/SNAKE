import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('data/fon.mp3')
pygame.mixer.music.play(loops=-1, start=0.0)
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

sb = 10
speed = 5
vol = 1.0
font_style = pygame.font.SysFont("bahnschrift", 25)  # Задаем шрифты
score_font = pygame.font.SysFont("comicsansms", 35)


def load_image(name, colorkey=None):
    fullname = 'data\\' + name
    # Если на диске не найден файл
    if not os.path.isfile(fullname):
        print(f'Файл с именем {fullname} не найден')
        sys.exit()
    # загрузить изображение из файла
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen(intro_text, file):
    # загрузить фон и изменить размеры изображения
    fon = pygame.transform.scale(load_image(file), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = font_style
    text_coord = 50
    for line in intro_text:  # Перебрать стриоки для вывода
        # создать графическое отображение строки (1 - сглаживание)
        string_rendered = font.render(line, 1, white)
        # прясмоугольня область для строки
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        # вывести на экран текст
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(speed)


def terminate():
    pygame.quit()
    sys.exit()


# Добавления счета
def Your_score(score):
    value = score_font.render("Счет: " + str(score), True, yellow)
    screen.blit(value, [0, 0])


# Отрисовка змеии
def our_snake(sb, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [int(x[0]), int(x[1]), sb, sb])


# вывод сообщения
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])


# Основная игра
def game():
    global speed, vol
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    schet = 2
    len_snake = 1
    pause = False
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

    foodx = round(random.randrange(0, WIDTH - sb) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - sb) / 10.0) * 10.0

    while not game_over:

        while game_close:
            screen.blit(fon, (0, 0))
            message("C Начать заного игру. Q закончить игру", red)
            Your_score(schet - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # Смещение
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -sb
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = sb
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -sb
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = sb
                    x1_change = 0
                elif event.key == pygame.K_w:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_e:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_p:
                    pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    pause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
        # Не вышел ли за границы
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.blit(fon, (0, 0))
        # формула отрисовки еды
        x = (sb // 2) + foodx
        y = (sb // 2) + foody
        pygame.draw.circle(screen, red, (int(x), int(y)), sb - 2)
        # отвечает за перемешение змеи
        sh = []
        sh.append(x1)
        sh.append(y1)
        snake_List.append(sh)
        if len(snake_List) > len_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == sh:
                game_close = True

        our_snake(sb, snake_List)
        Your_score(schet - 2)

        pygame.display.update()
        # Съел ли еду
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - sb) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - sb) / 10.0) * 10.0
            schet += 1
            len_snake = schet // 2
            if len_snake > 10:
                speed = len_snake // 2
        clock.tick(speed)
    start_screen(['Спасибо за то что играли в мою игру'], 'fon.jpg')
    pygame.quit()
    quit()


start_screen(['Змейка', 'Управление змейкой стрелки', 'Управление звуком W и E', 'P пауза'], 'fon.jpg')
game()
