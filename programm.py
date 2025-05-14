import os
import pygame
import random
import sqlite3
from pygame import Color
import os
import sys
from math import hypot
import time

class Border_1(pygame.sprite.Sprite):  # границы
   # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball1(pygame.sprite.Sprite):  # Враг
    def __init__(self, x, y, px, py):
        super().__init__(bullets)
        self.radius = 10
        radius = 10
        self.px = px
        self.py = py
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)

    def update(self):
        global health_1
        self.rect = self.rect.move(self.px, self.py)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.die()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.die()
        if pygame.sprite.collide_mask(self, hero):
            self.die()
            health_1 -= 1

    def die(self):
        self.kill()


class Ball2(pygame.sprite.Sprite):  # Свой
    def __init__(self, x, y, px, py):
        super().__init__(bullets)
        self.radius = 10
        radius = 10
        self.px = px
        self.py = py
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("yellow"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)

    def update(self):
        global boss_health
        self.rect = self.rect.move(self.px, self.py)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.die()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.die()
        if pygame.sprite.collide_mask(self, boss):
            self.die()
            boss_health -= 1

    def die(self):
        self.kill()

        
class Board:
    def __init__(self, spis):
        self.pole = spis
        self.n = 0

    def del_monster(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j] and 'm' in self.pole[i][j]:
                    self.pole[i][j] = 'x'

    def monster(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j] and 'm' in self.pole[i][j]:
                    return str(self.pole[i][j])[:-1]

    def del_chest(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j]:
                    pos = [i, j]
        self.pole[pos[0]][pos[1]] = 'x'

    def check_chest_name(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j] and 'c' in self.pole[i][j]:
                    return str(self.pole[i][j])[:-1]

    def chest(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j] and 'c' in self.pole[i][j]:
                    return True
        return False

    def vrag(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'm' in self.pole[i][j] and 'x' in self.pole[i][j]:
                    return True
        return False

    def zam(self, n):
        self.n = n

    def dv(self, x, y):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j]:
                    pos = [i, j]
        self.pole[pos[0]][pos[1]] = self.pole[pos[0]][pos[1]][:-1]
        self.pole[pos[0] - x][pos[1] - y] += 'x'

    def op(self, screen, adrs, x=0, y=0):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j]:
                    pos = [i, j]
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if abs(i - pos[0]) + abs(j - pos[1]) <= 7:
                    if self.pole[i][j] == '1':
                        pic = pygame.image.load("icons/stouns/kirpi.png")
                        screen.blit(pygame.transform.scale(pic, (80, 80)),
                                    ((i - pos[0] + 3) * 80 + 120 + x, (j - pos[1] + 3) * 80 + y))
                    if self.pole[i][j] != '1':
                        pic = pygame.image.load("icons/stouns/pesok.png")
                        screen.blit(pygame.transform.scale(pic, (80, 80)),
                                    ((i - pos[0] + 3) * 80 + 120 + x, (j - pos[1] + 3) * 80 + y))
                    if 'c' in self.pole[i][j]:
                        pic = pygame.image.load("icons/stouns/sun.png")
                        screen.blit(pygame.transform.scale(pic, (70, 70)),
                                    ((i - pos[0] + 3) * 80 + 120 + 5 + x, (j - pos[1] + 3) * 80 + 5 + y))
                    if 'y' in self.pole[i][j]:
                        pic = pygame.image.load("icons/portal.png")
                        screen.blit(pygame.transform.scale(pic, (70, 70)),
                                    ((i - pos[0] + 3) * 80 + 120 + 5 + x, (j - pos[1] + 3) * 80 + 5 + y))
                    if 'm' in self.pole[i][j]:
                        dd = self.pole[i][j].index('m') + 1
                        result = basa_cursor.execute('''SELECT * FROM Monster WHERE name = (?)''',
                                                     (str('m' + self.pole[i][j][dd]),)).fetchall()
                        pic = pygame.image.load(result[0][-1])
                        screen.blit(pygame.transform.scale(pic, (80, 80)),
                                    ((i - pos[0] + 3) * 80 + 120 + x, (j - pos[1] + 3) * 80 + y))
                    if 'x' in self.pole[i][j]:
                        p = [i, j]
        if self.n == 0:
            pic = pygame.image.load(adrs)
        else:
            pic = pygame.image.load(str(adrs[:-4] + '_r.png'))
        screen.blit(pygame.transform.scale(pic, (80, 80)), ((p[0] - pos[0] + 3) * 80 + 120, (p[1] - pos[1] + 3) * 80))

    def check(self, x, y):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j]:
                    pos = [i, j]
        if self.pole[pos[0] + y][pos[1] - x] != '1':
            return True
        else:
            return False
    def check_end(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if 'x' in self.pole[i][j]:
                    pos = [i, j]
        if 'y' in self.pole[pos[0]][pos[1]]:
            return True
        else:
            return False


class Border_2(pygame.sprite.Sprite):  # границы
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball3(pygame.sprite.Sprite):  # Враг
    def __init__(self, x, y, px, py):
        super().__init__(bullets)
        self.radius = 10
        radius = 10
        self.px = px
        self.py = py
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("green"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)

    def update(self):
        global health_1
        self.rect = self.rect.move(self.px, self.py)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.die()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.die()
        if pygame.sprite.collide_mask(self, hero):
            self.die()
            health_1 -= 1

    def die(self):
        self.kill()


class Ball4(pygame.sprite.Sprite):  # Свой
    def __init__(self, x, y, px, py):
        super().__init__(bullets)
        self.radius = 10
        radius = 10
        self.px = px
        self.py = py
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("yellow"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)

    def update(self):
        global boss_health_1
        self.rect = self.rect.move(self.px, self.py)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.die()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.die()
        if pygame.sprite.collide_mask(self, boss):
            self.die()
            boss_health_1 -= 1

    def die(self):
        self.kill()


def draw_health():
    global health_1
    for i in range(health_1):
        hearts = pygame.sprite.Group()
        hrt = pygame.sprite.Sprite()
        hrt.image = load_image('hearts.png')
        hrt.rect = hrt.image.get_rect()
        hrt.rect.y = 10
        hrt.rect.x = 30 * i + 10
        hearts.add(hrt)
        hearts.draw(screen)

def load_image(name, colorkey=None):  # Загрузка картинки
    fullname = name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def check(fraza_x):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        symbol_1 = pygame.K_a
        return str(fraza_x + 'a')
    if keys[pygame.K_b]:
        symbol_1 = pygame.K_b
        return str(fraza_x + 'b')
    if keys[pygame.K_c]:
        symbol_1 = pygame.K_c
        return str(fraza_x + 'c')
    if keys[pygame.K_d]:
        symbol_1 = pygame.K_d
        return str(fraza_x + 'd')
    if keys[pygame.K_e]:
        symbol_1 = pygame.K_e
        return str(fraza_x + 'e')
    if keys[pygame.K_f]:
        symbol_1 = pygame.K_f
        return str(fraza_x + 'f')
    if keys[pygame.K_g]:
        symbol_1 = pygame.K_g
        return str(fraza_x + 'g')
    if keys[pygame.K_h]:
        symbol_1 = pygame.K_h
        return str(fraza_x + 'h')
    if keys[pygame.K_i]:
        symbol_1 = pygame.K_i
        return str(fraza_x + 'i')
    if keys[pygame.K_j]:
        symbol_1 = pygame.K_j
        return str(fraza_x + 'j')
    if keys[pygame.K_k]:
        symbol_1 = pygame.K_k
        return str(fraza_x + 'k')
    if keys[pygame.K_l]:
        symbol_1 = pygame.K_l
        return str(fraza_x + 'l')
    if keys[pygame.K_m]:
        symbol_1 = pygame.K_m
        return str(fraza_x + 'm')
    if keys[pygame.K_n]:
        symbol_1 = pygame.K_n
        return str(fraza_x + 'n')
    if keys[pygame.K_o]:
        symbol_1 = pygame.K_o
        return str(fraza_x + 'o')
    if keys[pygame.K_p]:
        symbol_1 = pygame.K_p
        return str(fraza_x + 'p')
    if keys[pygame.K_q]:
        symbol_1 = pygame.K_q
        return str(fraza_x + 'q')
    if keys[pygame.K_r]:
        symbol_1 = pygame.K_r
        return str(fraza_x + 'r')
    if keys[pygame.K_s]:
        symbol_1 = pygame.K_s
        return str(fraza_x + 's')
    if keys[pygame.K_t]:
        symbol_1 = pygame.K_t
        return str(fraza_x + 't')
    if keys[pygame.K_u]:
        symbol_1 = pygame.K_u
        return str(fraza_x + 'u')
    if keys[pygame.K_v]:
        symbol_1 = pygame.K_v
        return str(fraza_x + 'v')
    if keys[pygame.K_w]:
        symbol_1 = pygame.K_w
        return str(fraza_x + 'w')
    if keys[pygame.K_x]:
        symbol_1 = pygame.K_x
        return str(fraza_x + 'x')
    if keys[pygame.K_y]:
        symbol_1 = pygame.K_y
        return str(fraza_x + 'y')
    if keys[pygame.K_z]:
        symbol_1 = pygame.K_z
        return str(fraza_x + 'z')
    if keys[pygame.K_BACKSPACE]:
        return str(fraza_x[:-1])
    return fraza_x


screen = pygame.display.set_mode((800, 600))
health_1 = 5
pygame.display.flip()
pygame.init()
running = True
fraza = 0
id_now_level = 0
fraza_1 = ''
fraza_2 = ''
stadia = 'gateway'
basa_d = sqlite3.connect('basa.db')
basa_cursor = basa_d.cursor()
id_people = 0
object_for_sell = 0
a = 1
now_hp = 100
while running:
    if stadia == 'gateway':
        screen.fill((0, 0, 0))
        pic = pygame.image.load("icons/registration.png")
        screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
        pic_people_1 = pygame.image.load("icons/registration_people_2.png")
        screen.blit(pygame.transform.scale(pic_people_1, (300, 300)), (-50, 300))
        pic_people_2 = pygame.image.load("icons/registration_people_1.png")
        screen.blit(pygame.transform.scale(pic_people_2, (300, 300)), (550, 300))
        head = pygame.image.load("icons/head.png")
        screen.blit(pygame.transform.scale(head, (150, 150)), (325, 50))
        play = pygame.image.load("icons/button.png")
        screen.blit(pygame.transform.scale(play, (250, 100)), (275, 350))
        play_2 = pygame.image.load("icons/button.png")
        screen.blit(pygame.transform.scale(play_2, (250, 100)), (550, 20))
        pygame.draw.rect(screen, (255, 100, 0), (250, 197, 300, 60), 4)
        pygame.draw.rect(screen, (255, 100, 0), (250, 265, 300, 60), 4)
        font_f = pygame.font.Font(None, 60)
        text = font_f.render('Войти', True, (0, 0, 0))
        screen.blit(text, (330, 380))
        font_f2 = pygame.font.Font(None, 45)
        text = font_f2.render('Регистрация', True, (0, 0, 0))
        screen.blit(text, (580, 55))
        font = pygame.font.Font(None, 60)
        if len(fraza_1) <= 8:
            text = font.render(fraza_1, True, (255, 150, 0))
        else:
            text = font.render('...' + fraza_1[-8:], True, (255, 150, 0))
        screen.blit(text, (255, 200))
        font2 = pygame.font.Font(None, 60)
        if len(fraza_2) <= 8:
            text2 = font2.render(fraza_2, True, (255, 150, 0))
        else:
            text2 = font.render('...' + fraza_2[-8:], True, (255, 150, 0))
        screen.blit(text2, (255, 270))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if fraza == 1:
                    fraza_1 = check(fraza_1)
                if fraza == 2:
                    fraza_2 = check(fraza_2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 250 < pos[0] < 550 and 197 < pos[1] < 257:
                    fraza = 1
                if 250 < pos[0] < 550 and 265 < pos[1] < 325:
                    fraza = 2
                if 570 < pos[0] < 780 and 40 < pos[1] < 100:
                    stadia = 'registration'
                if 300 < pos[0] < 500 and 365 < pos[1] < 470:
                    result = basa_cursor.execute('''SELECT * FROM Player WHERE login = (?) AND password = (?)''',
                                                 (fraza_1, fraza_2)).fetchall()
                    if len(result) == 1:
                        id_people = result[0][0]
                        stadia = 'main'
        if running:
            pygame.display.flip()

    if stadia == 'registration':
        screen.fill((0, 0, 0))
        pic = pygame.image.load("icons/registration.png")
        screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
        pic_people_1 = pygame.image.load("icons/registration_people_2.png")
        screen.blit(pygame.transform.scale(pic_people_1, (300, 300)), (-50, 300))
        pic_people_2 = pygame.image.load("icons/registration_people_1.png")
        screen.blit(pygame.transform.scale(pic_people_2, (300, 300)), (550, 300))
        head = pygame.image.load("icons/head.png")
        screen.blit(pygame.transform.scale(head, (150, 150)), (325, 50))
        play = pygame.image.load("icons/button.png")
        screen.blit(pygame.transform.scale(play, (300, 100)), (250, 350))
        pygame.draw.rect(screen, (255, 100, 0), (250, 197, 300, 60), 4)
        pygame.draw.rect(screen, (255, 100, 0), (250, 265, 300, 60), 4)
        font_f = pygame.font.Font(None, 50)
        text = font_f.render('Регистрация', True, (0, 0, 0))
        screen.blit(text, (295, 385))
        if len(fraza_1) <= 8:
            text = font.render(fraza_1, True, (255, 150, 0))
        else:
            text = font.render('...' + fraza_1[-8:], True, (255, 150, 0))
        screen.blit(text, (255, 200))
        font2 = pygame.font.Font(None, 60)
        if len(fraza_2) <= 8:
            text2 = font2.render(fraza_2, True, (255, 150, 0))
        else:
            text2 = font.render('...' + fraza_2[-8:], True, (255, 150, 0))
        screen.blit(text2, (255, 270))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if fraza == 1:
                    fraza_1 = check(fraza_1)
                if fraza == 2:
                    fraza_2 = check(fraza_2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 250 < pos[0] < 550 and 197 < pos[1] < 257:
                    fraza = 1
                if 250 < pos[0] < 550 and 265 < pos[1] < 325:
                    fraza = 2
                if 275 < pos[0] < 525 and 365 < pos[1] < 470:
                    result = basa_cursor.execute('''SELECT * FROM Player''').fetchall()
                    spis = []
                    for i in result:
                        spis.append(i[1])
                    if fraza_1 not in spis:
                        basa_cursor.execute('''INSERT INTO Player (login, password) VALUES (?, ?)''',
                                            (fraza_1, fraza_2))
                        basa_cursor.execute(
                            '''INSERT INTO Player_data (id_level, id_weapon,
                             id_armor, id_artifact, money) VALUES (?, ?, ?, ?, ?)''',
                            (1, 8, 6, 1, 0))
                        basa_d.commit()
                        result = list(basa_cursor.execute('''SELECT * FROM Player''').fetchall())
                        id_people = result[-1][0]
                        stadia = 'main'
        if running:
            pygame.display.flip()

    if stadia == 'main':
        a = 1
        now_hp = 100
        screen.fill((0, 0, 0))
        pic = pygame.image.load("icons/levels.png")
        screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
        result = list(
            basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
        pic = pygame.image.load(f"icons/people/a_{(result[0][3]) % 6 + 1}.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (25, 25))
        pic = pygame.image.load(f"icons/armor/armor_{result[0][3] % 6}.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (250, 100))
        pic = pygame.image.load(f"icons/weapon/weapon_{result[0][2] % 8}.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (250, 0))
        pic = pygame.image.load(f"icons/artifact/art_{result[0][4] % 7}.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (600, 50))
        pic = pygame.image.load("icons/shop.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (700, 500))
        result_w = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result[0][2],)).fetchall())
        result_a = list(basa_cursor.execute('''SELECT * FROM Artifact WHERE id = (?)''', (result[0][4],)).fetchall())
        result_b = list(basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result[0][3],)).fetchall())
        font = pygame.font.Font(None, 60)
        text = font.render(str(str(result_w[0][2]) + ' + ' + str(result_a[0][2])), True, (0, 0, 0))
        screen.blit(text, (360, 40))
        font2 = pygame.font.Font(None, 60)
        text2 = font2.render(str(str(result_b[0][2]) + ' + ' + str(result_a[0][3])), True, (0, 0, 0))
        screen.blit(text2, (360, 140))
        for i in range(1, 3):
            for j in range(1, 6):
                if result[0][1] >= (i - 1) * 5 + j:
                    if j == 5 and i == 1:
                        pic = pygame.image.load("icons/trees.png")
                        screen.blit(pygame.transform.scale(pic, (75, 75)), (j * 120, 250 if i == 1 else 400))
                    elif j == 5 and i == 2:
                        pic = pygame.image.load("icons/castle.png")
                        screen.blit(pygame.transform.scale(pic, (75, 75)), (j * 120, 250 if i == 1 else 400))
                    else:
                        pic = pygame.image.load("icons/hause.png")
                        screen.blit(pygame.transform.scale(pic, (75, 75)), (j * 120, 250 if i == 1 else 400))
                else:
                    if j == 5 and i == 1:
                        pic = pygame.image.load("icons/trees_b.png")
                        screen.blit(pygame.transform.scale(pic, (75, 75)), (j * 120, 250 if i == 1 else 400))
                    elif j == 5 and i == 2:
                        pic = pygame.image.load("icons/castle_b.png")
                        screen.blit(pygame.transform.scale(pic, (75, 75)), (j * 120, 250 if i == 1 else 400))
                    else:
                        pic = pygame.image.load("icons/hause_b.png")
                        screen.blit(pygame.transform.scale(pic, (75, 75)), (j * 120, 250 if i == 1 else 400))
                if i == 1:
                    font0 = pygame.font.Font(None, 40)
                    text0 = font0.render(str(i * j), True, (0, 0, 0))
                    screen.blit(text0, (j * 120 + 75, 300 if i == 1 else 450))
                else:
                    font0 = pygame.font.Font(None, 40)
                    text0 = font0.render(str(5 + j), True, (0, 0, 0))
                    screen.blit(text0, (j * 120 + 75, 300 if i == 1 else 450))
        font_m = pygame.font.Font(None, 60)
        text_m = font_m.render(str('$') + str(result[0][-1]), True, (0, 0, 0))
        screen.blit(text_m, (500, 550))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = list(event.pos)
                if 325 > pos[1] > 250 and 120 < pos[0] < 195:
                    if result[0][1] >= 1:
                        stadia = 'play'
                        id_now_level = 1
                if 325 > pos[1] > 250 and 240 < pos[0] < 315:
                    if result[0][1] >= 2:
                        stadia = 'play'
                        id_now_level = 2
                if 325 > pos[1] > 250 and 360 < pos[0] < 435:
                    if result[0][1] >= 3:
                        stadia = 'play'
                        id_now_level = 3
                if 325 > pos[1] > 250 and 480 < pos[0] < 555:
                    if result[0][1] >= 4:
                        stadia = 'play'
                        id_now_level = 4
                if 325 > pos[1] > 250 and 600 < pos[0] < 675:
                    if result[0][1] >= 5:
                        stadia = 'play'
                        id_now_level = 5
                if 475 > pos[1] > 400 and 120 < pos[0] < 195:
                    if result[0][1] >= 6:
                        stadia = 'play'
                        id_now_level = 6
                if 475 > pos[1] > 400 and 240 < pos[0] < 315:
                    if result[0][1] >= 7:
                        stadia = 'play'
                        id_now_level = 7
                if 475 > pos[1] > 400 and 360 < pos[0] < 435:
                    if result[0][1] >= 8:
                        stadia = 'play'
                        id_now_level = 8
                if 475 > pos[1] > 400 and 480 < pos[0] < 555:
                    if result[0][1] >= 9:
                        stadia = 'play'
                        id_now_level = 9
                if 475 > pos[1] > 400 and 600 < pos[0] < 675:
                    if result[0][1] >= 10:
                        stadia = 'play'
                        id_now_level = 10
                if 600 > pos[1] > 500 and 700 < pos[0] < 800:
                    stadia = 'buy'
        if running:
            pygame.display.flip()
    if stadia == 'buy':
        screen.fill((0, 0, 0))
        pic = pygame.image.load("icons/pp.png")
        screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
        pic = pygame.image.load("icons/shop_exit.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (670, 30))
        result = list(
            basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (50, 25))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (250, 25))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (50, 225))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (250, 225))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (450, 25))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (450, 225))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (450, 425))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (250, 425))
        pic = pygame.image.load("icons/ramka.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (50, 425))
        pic = pygame.image.load("icons/weapon/weapon_3.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (75, 50))
        pic = pygame.image.load("icons/weapon/weapon_5.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (275, 50))
        pic = pygame.image.load("icons/weapon/weapon_6.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (475, 50))
        pic = pygame.image.load("icons/armor/armor_2.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (75, 250))
        pic = pygame.image.load("icons/armor/armor_3.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (275, 250))
        pic = pygame.image.load("icons/armor/armor_4.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (475, 250))
        pic = pygame.image.load("icons/artifact/art_4.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (475, 450))
        pic = pygame.image.load("icons/artifact/art_3.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (275, 450))
        pic = pygame.image.load("icons/artifact/art_2.png")
        screen.blit(pygame.transform.scale(pic, (100, 100)), (75, 450))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 50 < pos[0] < 200 and 25 < pos[1] < 175:
                    stadia = 'sell'
                    object_for_sell = 1
                if 250 < pos[0] < 400 and 25 < pos[1] < 175:
                    stadia = 'sell'
                    object_for_sell = 2
                if 450 < pos[0] < 600 and 25 < pos[1] < 175:
                    stadia = 'sell'
                    object_for_sell = 3
                if 50 < pos[0] < 200 and 225 < pos[1] < 375:
                    stadia = 'sell'
                    object_for_sell = 4
                if 250 < pos[0] < 400 and 225 < pos[1] < 375:
                    stadia = 'sell'
                    object_for_sell = 5
                if 450 < pos[0] < 600 and 225 < pos[1] < 375:
                    stadia = 'sell'
                    object_for_sell = 6
                if 50 < pos[0] < 200 and 425 < pos[1] < 575:
                    stadia = 'sell'
                    object_for_sell = 7
                if 250 < pos[0] < 400 and 425 < pos[1] < 575:
                    stadia = 'sell'
                    object_for_sell = 8
                if 450 < pos[0] < 600 and 425 < pos[1] < 575:
                    stadia = 'sell'
                    object_for_sell = 9
                if 670 < pos[0] < 770 and 30 < pos[1] < 130:
                    stadia = 'main'
        if running:
            pygame.display.flip()
    if stadia == 'sell':
        screen.fill((0, 0, 0))
        pic = pygame.image.load("icons/pp.png")
        screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
        result = list(
            basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
        ttt1 = 'Желаете купить '
        ttt3 = ' за '
        pic = pygame.image.load("icons/krest.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (550, 400))
        pic = pygame.image.load("icons/plus.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (350, 400))
        if object_for_sell == 1:
            ttt2 = 'деревянный топор'
            ttt4 = '1000'
            pic = pygame.image.load("icons/weapon/weapon_3.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Урон - 30'), True, (0, 0, 0))
            screen.blit(text, (350, 250))
        if object_for_sell == 2:
            ttt2 = 'железный топор'
            ttt4 = '15000'
            pic = pygame.image.load("icons/weapon/weapon_5.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Урон - 50'), True, (0, 0, 0))
            screen.blit(text, (350, 250))
        if object_for_sell == 3:
            ttt2 = 'железный меч'
            ttt4 = '50000'
            pic = pygame.image.load("icons/weapon/weapon_6.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Урон - 75'), True, (0, 0, 0))
            screen.blit(text, (350, 250))
        if object_for_sell == 4:
            ttt2 = 'броню гоплита'
            ttt4 = '2000'
            pic = pygame.image.load("icons/armor/armor_2.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Защита - 15'), True, (0, 0, 0))
            screen.blit(text, (350, 250))
        if object_for_sell == 5:
            ttt2 = 'комплект омоновца'
            ttt4 = '10000'
            pic = pygame.image.load("icons/armor/armor_3.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Защита - 25'), True, (0, 0, 0))
            screen.blit(text, (350, 250))
        if object_for_sell == 6:
            ttt2 = 'железную броню'
            ttt4 = '30000'
            pic = pygame.image.load("icons/armor/armor_4.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Защита - 50'), True, (0, 0, 0))
            screen.blit(text, (350, 250))
        if object_for_sell == 7:
            ttt2 = 'раномайзер'
            ttt4 = '2000'
            pic = pygame.image.load("icons/artifact/art_2.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Урон - 15'), True, (0, 0, 0))
            screen.blit(text, (350, 150))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Защита - 10'), True, (0, 0, 0))
            screen.blit(text, (350, 255))
        if object_for_sell == 8:
            ttt2 = 'рубиновое кольцо'
            ttt4 = '4000'
            pic = pygame.image.load("icons/artifact/art_3.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Урон - 30'), True, (0, 0, 0))
            screen.blit(text, (350, 150))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Защита - 15'), True, (0, 0, 0))
            screen.blit(text, (350, 225))
        if object_for_sell == 9:
            ttt2 = 'браслет земли'
            ttt4 = '5000'
            pic = pygame.image.load("icons/artifact/art_4.png")
            screen.blit(pygame.transform.scale(pic, (200, 200)), (50, 200))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Урон - 0'), True, (0, 0, 0))
            screen.blit(text, (350, 150))
            font = pygame.font.Font(None, 100)
            text = font.render(str('Защита - 40'), True, (0, 0, 0))
            screen.blit(text, (350, 225))
        font = pygame.font.Font(None, 60)
        text = font.render(str(ttt1 + ttt2), True, (0, 0, 0))
        screen.blit(text, (50, 50))
        font = pygame.font.Font(None, 60)
        text = font.render(str(ttt3 + '$' + ttt4 + '?'), True, (0, 0, 0))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 350 < pos[0] < 500 and 400 < pos[1] < 550:
                    stadia == 'buy'
                    if result[0][-1] >= int(ttt4):
                        if object_for_sell == 1:
                            basa_cursor.execute("""UPDATE Player_data SET id_weapon = (?) WHERE id_people = (?)""",
                                                (3, id_people))
                            basa_d.commit()
                        if object_for_sell == 2:
                            basa_cursor.execute("""UPDATE Player_data SET id_weapon = (?) WHERE id_people = (?)""",
                                                (5, id_people))
                            basa_d.commit()
                        if object_for_sell == 3:
                            basa_cursor.execute("""UPDATE Player_data SET id_weapon = (?) WHERE id_people = (?)""",
                                                (6, id_people))
                            basa_d.commit()
                        if object_for_sell == 4:
                            basa_cursor.execute("""UPDATE Player_data SET id_armor = (?) WHERE id_people = (?)""",
                                                (2, id_people))
                            basa_d.commit()
                        if object_for_sell == 5:
                            basa_cursor.execute("""UPDATE Player_data SET id_armor = (?) WHERE id_people = (?)""",
                                                (3, id_people))
                            basa_d.commit()
                        if object_for_sell == 6:
                            basa_cursor.execute("""UPDATE Player_data SET id_armor = (?) WHERE id_people = (?)""",
                                                (4, id_people))
                            basa_d.commit()
                        if object_for_sell == 7:
                            basa_cursor.execute("""UPDATE Player_data SET id_artifact = (?) WHERE id_people = (?)""",
                                                (2, id_people))
                            basa_d.commit()
                        if object_for_sell == 8:
                            basa_cursor.execute("""UPDATE Player_data SET id_artifact = (?) WHERE id_people = (?)""",
                                                (3, id_people))
                            basa_d.commit()
                        if object_for_sell == 9:
                            basa_cursor.execute("""UPDATE Player_data SET id_artifact = (?) WHERE id_people = (?)""",
                                                (4, id_people))
                            basa_d.commit()
                        basa_cursor.execute("""UPDATE Player_data SET money = (?) WHERE id_people = (?)""",
                                            (result[0][-1] - int(ttt4), id_people))
                        basa_d.commit()
                        stadia = 'buy'
                if 550 < pos[0] < 700 and 400 < pos[1] < 550:
                    stadia = 'buy'
        if running:
            pygame.display.flip()
    if stadia == 'play':
        screen.fill((0, 0, 0))
        pic = pygame.image.load("icons/labirint.png")
        pic2 = pygame.image.load("icons/pp.png")
        pic3 = pygame.image.load("icons/pp.png")
        screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
        result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
        if a == 1:
            level = []
            f = list(open(f'levels/level_{id_now_level}.txt'))
            for i in f:
                level.append(i.strip().split())
            board = Board(level)
            a = 0
        adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
        board.op(screen, adrs)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pos[0] < 785 and pos[0] > 695 and pos[1] > 390 and pos[1] < 480:
                    stadia = 'main'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if board.check(1, 0):
                        for i in range(4):
                            adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                            screen.fill((0, 0, 0))
                            screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
                            board.op(screen, adrs, 0, 20 * i)
                            result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
                            screen.blit(pygame.transform.scale(pic3, (120, 600)), (680, 0))
                            screen.blit(pygame.transform.scale(pic2, (120, 600)), (0, 0))
                            adrs = f'icons/weapon/weapon_{(result[0][2]) % 8}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 50))
                            adrs = f'icons/armor/armor_{(result[0][3]) % 6}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 220))
                            adrs = f'icons/artifact/art_{(result[0][4]) % 7}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 390))
                            p = pygame.image.load('icons/serdce.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 50))
                            p = pygame.image.load('icons/shop_exit.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 390))
                            font = pygame.font.Font(None, 40)
                            text = font.render(str('HP - ' + str(now_hp)), True, (0, 0, 0))
                            screen.blit(text, (685, 155))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result[0][2],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (3, 160))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result[0][3],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 350))
                            pygame.display.flip()
                            result2 = list(basa_cursor.execute('''SELECT * FROM Artifact WHERE id = (?)''', (result[0][4],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 500))
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][3]), True, (0, 0, 0))
                            screen.blit(text, (1, 560))
                            pygame.display.flip()
                        board.dv(0, 1)
                    adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                    board.op(screen, adrs)
                if event.key == pygame.K_s:
                    if board.check(-1, 0):
                        for i in range(4):
                            adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                            screen.fill((0, 0, 0))
                            screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
                            board.op(screen, adrs, 0, -20 * i)
                            result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
                            screen.blit(pygame.transform.scale(pic3, (120, 600)), (680, 0))
                            screen.blit(pygame.transform.scale(pic2, (120, 600)), (0, 0))
                            adrs = f'icons/weapon/weapon_{(result[0][2]) % 8}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 50))
                            adrs = f'icons/armor/armor_{(result[0][3]) % 6}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 220))
                            adrs = f'icons/artifact/art_{(result[0][4]) % 7}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 390))
                            p = pygame.image.load('icons/serdce.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 50))
                            p = pygame.image.load('icons/shop_exit.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 390))
                            font = pygame.font.Font(None, 40)
                            text = font.render(str('HP - ' + str(now_hp)), True, (0, 0, 0))
                            screen.blit(text, (685, 155))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result[0][2],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (3, 160))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result[0][3],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 350))
                            pygame.display.flip()
                            result2 = list(basa_cursor.execute('''SELECT * FROM Artifact WHERE id = (?)''', (result[0][4],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 500))
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][3]), True, (0, 0, 0))
                            screen.blit(text, (1, 560))
                            pygame.display.flip()
                        board.dv(0, -1)
                    adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                    board.op(screen, adrs)
                if event.key == pygame.K_a:
                    board.zam(1)
                    if board.check(0, -1):
                        for i in range(4):
                            adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                            screen.fill((0, 0, 0))
                            screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
                            board.op(screen, adrs, 20 * i, 0)
                            result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
                            screen.blit(pygame.transform.scale(pic3, (120, 600)), (680, 0))
                            screen.blit(pygame.transform.scale(pic2, (120, 600)), (0, 0))
                            adrs = f'icons/weapon/weapon_{(result[0][2]) % 8}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 50))
                            adrs = f'icons/armor/armor_{(result[0][3]) % 6}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 220))
                            adrs = f'icons/artifact/art_{(result[0][4]) % 7}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 390))
                            p = pygame.image.load('icons/serdce.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 50))
                            p = pygame.image.load('icons/shop_exit.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 390))
                            font = pygame.font.Font(None, 40)
                            text = font.render(str('HP - ' + str(now_hp)), True, (0, 0, 0))
                            screen.blit(text, (685, 155))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result[0][2],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (3, 160))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result[0][3],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 350))
                            pygame.display.flip()
                            result2 = list(basa_cursor.execute('''SELECT * FROM Artifact WHERE id = (?)''', (result[0][4],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 500))
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][3]), True, (0, 0, 0))
                            screen.blit(text, (1, 560))
                            pygame.display.flip()
                        board.dv(1, 0)
                    adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                    board.op(screen, adrs)
                if event.key == pygame.K_d:
                    board.zam(0)
                    if board.check(0, 1):
                        for i in range(4):
                            adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                            screen.fill((0, 0, 0))
                            screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
                            board.op(screen, adrs, -20 * i, 0)
                            result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
                            screen.blit(pygame.transform.scale(pic3, (120, 600)), (680, 0))
                            screen.blit(pygame.transform.scale(pic2, (120, 600)), (0, 0))
                            adrs = f'icons/weapon/weapon_{(result[0][2]) % 8}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 50))
                            adrs = f'icons/armor/armor_{(result[0][3]) % 6}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 220))
                            adrs = f'icons/artifact/art_{(result[0][4]) % 7}.png'
                            p = pygame.image.load(adrs)
                            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 390))
                            p = pygame.image.load('icons/serdce.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 50))
                            p = pygame.image.load('icons/shop_exit.png')
                            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 390))
                            font = pygame.font.Font(None, 40)
                            text = font.render(str('HP - ' + str(now_hp)), True, (0, 0, 0))
                            screen.blit(text, (685, 155))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result[0][2],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (3, 160))
                            result2 = list(basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result[0][3],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 350))
                            pygame.display.flip()
                            result2 = list(basa_cursor.execute('''SELECT * FROM Artifact WHERE id = (?)''', (result[0][4],)).fetchall())
                            font = pygame.font.Font(None, 38)
                            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
                            screen.blit(text, (1, 500))
                            font = pygame.font.Font(None, 38)
                            text = font.render('Броня ' + str(result2[0][3]), True, (0, 0, 0))
                            screen.blit(text, (1, 560))
                            pygame.display.flip() 
                        board.dv(-1, 0)
                    adrs = f'icons/people/a_{(result[0][3] % 6) + 1}.png'
                    board.op(screen, adrs)
        if board.chest():
            stadia = 'chest'
            name_of_chest = board.check_chest_name()
            result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
            result1 = list(basa_cursor.execute('''SELECT * FROM Chest WHERE name = (?)''', (name_of_chest,)).fetchall())
            result2 = list(basa_cursor.execute('''SELECT * FROM Chest_Subject WHERE id_chest = (?)''', (result1[0][0],)).fetchall())
        if board.vrag():
            stadia = 'vrag'
        if board.monster() == 'm9':
            stadia = 'boss_1'
        if board.monster() == 'mz':
            stadia = 'boss_2'
        if board.check_end():
            stadia = 'main'
            basa_cursor.execute("""UPDATE Player_data SET id_level = (?) WHERE id_people = (?)""", (max(id_now_level + 1, result[0][1]), id_people))
            basa_d.commit()
        if running:
            result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
            screen.blit(pygame.transform.scale(pic3, (120, 600)), (680, 0))
            screen.blit(pygame.transform.scale(pic2, (120, 600)), (0, 0))
            adrs = f'icons/weapon/weapon_{(result[0][2]) % 8}.png'
            p = pygame.image.load(adrs)
            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 50))
            adrs = f'icons/armor/armor_{(result[0][3]) % 6}.png'
            p = pygame.image.load(adrs)
            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 220))
            adrs = f'icons/artifact/art_{(result[0][4]) % 7}.png'
            p = pygame.image.load(adrs)
            screen.blit(pygame.transform.scale(p, (90, 90)), (15, 390))
            p = pygame.image.load('icons/serdce.png')
            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 50))
            p = pygame.image.load('icons/shop_exit.png')
            screen.blit(pygame.transform.scale(p, (90, 90)), (695, 390))
            font = pygame.font.Font(None, 40)
            text = font.render(str('HP - ' + str(now_hp)), True, (0, 0, 0))
            screen.blit(text, (685, 155))
            result2 = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result[0][2],)).fetchall())
            font = pygame.font.Font(None, 38)
            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
            screen.blit(text, (3, 160))
            result2 = list(basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result[0][3],)).fetchall())
            font = pygame.font.Font(None, 38)
            text = font.render('Броня ' + str(result2[0][2]), True, (0, 0, 0))
            screen.blit(text, (1, 350))
            pygame.display.flip()
            result2 = list(basa_cursor.execute('''SELECT * FROM Artifact WHERE id = (?)''', (result[0][4],)).fetchall())
            font = pygame.font.Font(None, 38)
            text = font.render('Урон ' + str(result2[0][2]), True, (0, 0, 0))
            screen.blit(text, (1, 500))
            font = pygame.font.Font(None, 38)
            text = font.render('Броня ' + str(result2[0][3]), True, (0, 0, 0))
            screen.blit(text, (1, 560))
            pygame.display.flip()
    if stadia == 'chest':
        result2 = list(basa_cursor.execute('''SELECT * FROM Chest_Subject WHERE id_chest = (?)''', (result1[0][0],)).fetchall())
        screen.fill((0, 0, 0))
        pic = pygame.image.load("icons/pp.png")
        screen.blit(pygame.transform.scale(pic, (800, 600)), (0, 0))
        pic = pygame.image.load("icons/krest.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (550, 400))
        pic = pygame.image.load("icons/plus.png")
        screen.blit(pygame.transform.scale(pic, (150, 150)), (350, 400))
        if result2[0][1] != 0:
            res = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result2[0][1],)).fetchall())
            font = pygame.font.Font(None, 60)
            text = font.render(str('Желаете подобрать? ' + str('Урон ' + str(res[0][2]))), True, (0, 0, 0))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 60)
            text = font.render(str(res[0][1]), True, (0, 0, 0))
            screen.blit(text, (20, 370))
            pic = pygame.image.load(str(res[0][-1]) + '.png')
            screen.blit(pygame.transform.scale(pic, (100, 100)), (100, 250))
            thing = 1
        if result2[0][2] != 0:
            res = list(basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result2[0][2],)).fetchall())
            font = pygame.font.Font(None, 60)
            text = font.render(str('Желаете подобрать? ' + str('Защита ' + str(res[0][2]))), True, (0, 0, 0))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 60)
            text = font.render(str(res[0][1]), True, (0, 0, 0))
            screen.blit(text, (20, 370))
            pic = pygame.image.load(str(res[0][-1]) + '.png')
            screen.blit(pygame.transform.scale(pic, (100, 100)), (100, 250))
            thing = 2
        if result2[0][3] != 0:
            res = list(basa_cursor.execute('''SELECT * FROM Artifact WHERE id = (?)''', (result2[0][3],)).fetchall())
            font = pygame.font.Font(None, 60)
            text = font.render(str('Желаете подобрать? ' + str('Защита ' + str(res[0][3]))), True, (0, 0, 0))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 60)
            text = font.render(str(str('Атака ' + str(res[0][2]))), True, (0, 0, 0))
            screen.blit(text, (50, 170))
            font = pygame.font.Font(None, 60)
            text = font.render(str(res[0][1]), True, (0, 0, 0))
            screen.blit(text, (20, 370))
            pic = pygame.image.load(str(res[0][-1]) + '.png')
            screen.blit(pygame.transform.scale(pic, (100, 100)), (100, 250))
            thing = 3
        if result2[0][4] != 0:
            res = result2[0][4]
            font = pygame.font.Font(None, 60)
            text = font.render(str('Желаете подобрать? ' + str(res)), True, (0, 0, 0))
            screen.blit(text, (50, 100))
            font = pygame.font.Font(None, 60)
            text = font.render(str('Монеты'), True, (0, 0, 0))
            screen.blit(text, (20, 370))
            pic = pygame.image.load('icons/money.png')
            screen.blit(pygame.transform.scale(pic, (150, 150)), (100, 200))
            thing = 4
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pos[0] < 700 and pos[0] > 550 and pos[1] > 400 and pos[1] < 550:
                    stadia = 'play'
                    board.del_chest()
                if pos[0] < 500 and pos[0] > 350 and pos[1] > 400 and pos[1] < 550:
                    stadia = 'play'
                    board.del_chest()
                    if thing == 1:
                        basa_cursor.execute("""UPDATE Player_data SET id_weapon = (?) WHERE id_people = (?)""", (result2[0][1], id_people))
                        basa_d.commit()
                    if thing == 2:
                        basa_cursor.execute("""UPDATE Player_data SET id_armor = (?) WHERE id_people = (?)""", (result2[0][2], id_people))
                        basa_d.commit()
                    if thing == 3:
                        basa_cursor.execute("""UPDATE Player_data SET id_artifact = (?) WHERE id_people = (?)""", (result2[0][3], id_people))
                        basa_d.commit()
                    if thing == 4:
                        result = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
                        basa_cursor.execute("""UPDATE Player_data SET money = (?) WHERE id_people = (?)""", (int(result[0][-1] + result2[0][4]), id_people))
                        basa_d.commit()
        if running:
            pygame.display.flip()
    if stadia == 'vrag':
        result = list(basa_cursor.execute('''SELECT * FROM Monster WHERE name = (?)''', (board.monster(),)).fetchall())
        result1 = list(basa_cursor.execute('''SELECT * FROM Player_data WHERE id_people = (?)''', (id_people,)).fetchall())
        result2 = list(basa_cursor.execute('''SELECT * FROM Weapon WHERE id = (?)''', (result1[0][2],)).fetchall())
        result3 = basa_cursor.execute('''SELECT * FROM Armor WHERE id = (?)''', (result1[0][3],)).fetchall()
        m_hp = result[0][2]
        while (m_hp > 0) and (now_hp > 0):
            now_hp -= max(result[0][3] - result3[0][2], 0)
            m_hp -= result2[0][2]
        board.del_monster()
        if now_hp > 0:
            stadia = 'play'
        else:
            stadia = 'die'
    if stadia == 'die':
        screen.fill((150, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (250, 250, 300, 60), 4)
        font = pygame.font.Font(None, 40)
        text = font.render(str('В меню'), True, (0, 0, 0))
        screen.blit(text, (300, 260))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pos[0] > 250 and pos[0] < 550 and pos[0] > 250 and pos[0] > 310:
                    stadia = 'main'
        if running:
            pygame.display.flip()
    if stadia == 'boss_1':
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Лабиринт монстров')

        fps = 60  # количество кадров в секунду
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        cur_sprite = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()
        fon = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        width = 800
        height = 600
        boss_health_1 = 50
        health_1 = 5

        Border_2(0, 0, width, 0)
        Border_2(0, height, width, height)
        Border_2(0, 0, 0, height)
        Border_2(width, 0, width, height)

        fonn = pygame.sprite.Sprite()
        fonn.image = load_image("area2.jpg")  # поправить
        fonn.rect = fonn.image.get_rect()
        fon.add(fonn)

        cursor = pygame.sprite.Sprite()  # Спрайт курсора
        cursor.image = load_image("shoot.png")
        cursor.rect = cursor.image.get_rect()
        cur_sprite.add(cursor)

        hero = pygame.sprite.Sprite()  # Герой
        hero.image = load_image("hero.png")
        hero.rect = hero.image.get_rect()
        hero.rect.x = 350
        hero.rect.y = 500
        all_sprites.add(hero)

        boss = pygame.sprite.Sprite()  # Босс
        boss.image = load_image("boss2.png")
        boss.rect = boss.image.get_rect()
        boss.rect.x = 300
        boss.rect.y = 10
        all_sprites.add(boss)

        skull = pygame.sprite.Sprite()
        skull.image = load_image('skul.png')
        skull.rect = skull.image.get_rect()
        skull.rect.x = 770
        skull.rect.y = 5
        all_sprites.add(skull)

        running2 = True
        game = True
        boss_view_1 = 1
        hero_view_1 = 1
        boss_delta_1 = 1
        boss_delta_2_1 = 5
        count_boss_delta_1 = 5
        delta_boss_bullet_1 = 40
        direction = (0, 0)

        while running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                    pygame.quit()
                if pygame.mouse.get_focused():
                    pos = pygame.mouse.get_pos()
                    x, y = pygame.mouse.get_pos()
                    cursor.rect.x = x - 10
                    cursor.rect.y = y - 10
                    fon.draw(screen)
                    cur_sprite.draw(screen)
                    if cursor.rect.x < hero.rect.x and hero_view_1 == 1:
                        hero_view_1 = 2
                        im = pygame.transform.flip(hero.image, True, False)
                        hero.image = im
                    if cursor.rect.x > hero.rect.x and hero_view_1 == 2:
                        hero_view_1 = 1
                        im = pygame.transform.flip(hero.image, True, False)
                        hero.image = im
                if event.type == pygame.KEYDOWN and game:
                    if event.key in (pygame.K_UP, 119):
                        direction = (0, -4)
                    elif event.key in (pygame.K_DOWN, 115):
                        direction = (0, 4)
                    elif event.key in (pygame.K_RIGHT, 100):
                        direction = (4, 0)
                    elif event.key in (pygame.K_LEFT, 97):
                        direction = (-4, 0)
                if event.type == pygame.KEYUP:
                    direction = (0, 0)
                if event.type == pygame.MOUSEBUTTONDOWN and game:
                    if event.button == 1:
                        delta1 = event.pos[0] - hero.rect.x
                        delta2 = event.pos[1] - hero.rect.y
                        d = round(hypot(delta1, delta2))
                        delta_x = 10 * delta1 / d
                        delta_y = 10 * delta2 / d

                        Ball4(hero.rect.x + 20, hero.rect.y - 10, delta_x, delta_y)

            if 0 < hero.rect.x + direction[0] <= 740:
                hero.rect.x += direction[0]
            if 0 < hero.rect.y + direction[1] <= 524:
                hero.rect.y += direction[1]
            if pygame.sprite.collide_mask(hero, boss):
                direction = (0, 0)
                health_1 -= 1
                hero.rect.x = 350
                hero.rect.y = 500

            delta_boss_bullet_1 -= 1
            if not delta_boss_bullet_1 and game:
                delta_boss_bullet_1 = 20
                if boss_view_1 == 1:
                    delta1 = hero.rect.x + 10 - (boss.rect.x + 20)
                    delta2 = hero.rect.y - 10 - (boss.rect.y + 220)
                else:
                    delta1 = hero.rect.x + 10 - (boss.rect.x + 150)
                    delta2 = hero.rect.y - 10 - (boss.rect.y + 220)
                d = round(hypot(delta1, delta2))
                delta_x = 5 * delta1 / d
                delta_y = 5 * delta2 / d
                if boss_view_1 == 1:
                    Ball3(boss.rect.x + 20, boss.rect.y + 220, delta_x, delta_y)
                else:
                    Ball3(boss.rect.x + 150, boss.rect.y + 220, delta_x, delta_y)

            if boss.rect.y in (1, 10):
                boss_delta_1 *= -1
            if boss.rect.x in (50, 600):
                boss_delta_2_1 *= -1
            boss.rect.x += boss_delta_2_1
            boss.rect.y += boss_delta_1
            count_boss_delta_1 -= 1
            if count_boss_delta_1 == 0:
                boss.rect.y += boss_delta_1
                count_boss_delta_1 = 5
            if boss.rect.x < hero.rect.x and boss_view_1 == 1:
                boss_view_1 = 2
                im = pygame.transform.flip(boss.image, True, False)
                boss.image = im
            if boss.rect.x > hero.rect.x and boss_view_1 == 2:
                boss_view_1 = 1
                im = pygame.transform.flip(boss.image, True, False)
                boss.image = im
            #  старт отрисовки
            if pygame.mouse.get_focused():
                fon.draw(screen)
                if game:
                    bullets.update()
                    bullets.draw(screen)
                all_sprites.update()
                all_sprites.draw(screen)
                draw_health()
                pygame.draw.rect(screen, Color('black'), (550, 5, 210, 30))
                pygame.draw.rect(screen, Color('red'), (555, 10, boss_health_1 * 4, 20))
                cur_sprite.draw(screen)
            elif not pygame.mouse.get_focused():
                fon.draw(screen)
                if game:
                    bullets.update()
                    bullets.draw(screen)
                all_sprites.update()
                all_sprites.draw(screen)
                draw_health()
                pygame.draw.rect(screen, Color('black'), (550, 5, 210, 30))
                pygame.draw.rect(screen, Color('red'), (555, 10, boss_health_1 * 4, 20))
            if not health_1 or not boss_health_1:
                new = pygame.sprite.Group()
                game = False
                fin = pygame.sprite.Sprite()
                if not health_1:
                    fin.image = load_image('defeat.png')
                    a = 'd'
                    fin.rect = fin.image.get_rect()
                    fin.rect.x = 225
                    fin.rect.y = 100
                if not boss_health_1:
                    fin.image = load_image('victory.png')
                    a = 'v'
                    fin.rect = fin.image.get_rect()
                    fin.rect.x = 100
                    fin.rect.y = 100
                new.add(fin)
                new.draw(screen)
                pygame.display.flip()
                time.sleep(1)
                running2 = False
                if a == 'd':
                    stadia = 'main'
                if a == 'v':
                    stadia = 'play'

            pygame.display.flip()
            clock.tick(fps)
        if a == 'd':
            stadia = 'main'
        if a == 'v':
            stadia = 'play'
        board.del_monster()
        pygame.mouse.set_visible(True)

    if stadia == 'boss_2':
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Лабиринт минотавра')

        fps = 60  # количество кадров в секунду
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        cur_sprite = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()
        fon = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        width = 800
        height = 600
        boss_health = 100
        health_1 = 5

        Border_1(0, 0, width, 0)
        Border_1(0, height, width, height)
        Border_1(0, 0, 0, height)
        Border_1(width, 0, width, height)

        fonn = pygame.sprite.Sprite()
        fonn.image = load_image("area.jpg")
        fonn.rect = fonn.image.get_rect()
        fon.add(fonn)

        cursor = pygame.sprite.Sprite()  # Спрайт курсора
        cursor.image = load_image("shoot.png")
        cursor.rect = cursor.image.get_rect()
        cur_sprite.add(cursor)

        hero = pygame.sprite.Sprite()  # Герой
        hero.image = load_image("hero.png")
        hero.rect = hero.image.get_rect()
        hero.rect.x = 350
        hero.rect.y = 500
        all_sprites.add(hero)

        boss = pygame.sprite.Sprite()  # Босс
        boss.image = load_image("boss1.png")
        boss.rect = boss.image.get_rect()
        boss.rect.x = 300
        boss.rect.y = 10
        all_sprites.add(boss)

        skull = pygame.sprite.Sprite()
        skull.image = load_image('skul.png')
        skull.rect = skull.image.get_rect()
        skull.rect.x = 770
        skull.rect.y = 5
        all_sprites.add(skull)

        running3 = True
        game = True
        boss_view = 1
        hero_view = 1
        boss_delta = 1
        boss_delta_2 = 5
        count_boss_delta = 5
        delta_boss_bullet = 20
        direction = (0, 0)

        while running3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running3 = False
                    pygame.quit()
                if pygame.mouse.get_focused():
                    pos = pygame.mouse.get_pos()
                    x, y = pygame.mouse.get_pos()
                    cursor.rect.x = x - 10
                    cursor.rect.y = y - 10
                    fon.draw(screen)
                    cur_sprite.draw(screen)
                    if cursor.rect.x < hero.rect.x and hero_view == 1:
                        hero_view = 2
                        im = pygame.transform.flip(hero.image, True, False)
                        hero.image = im
                    if cursor.rect.x > hero.rect.x and hero_view == 2:
                        hero_view = 1
                        im = pygame.transform.flip(hero.image, True, False)
                        hero.image = im
                if event.type == pygame.KEYDOWN and game:
                    if event.key in (pygame.K_UP, 119):
                        direction = (0, -5)
                    elif event.key in (pygame.K_DOWN, 115):
                        direction = (0, 5)
                    elif event.key in (pygame.K_RIGHT, 100):
                        direction = (5, 0)
                    elif event.key in (pygame.K_LEFT, 97):
                        direction = (-5, 0)
                if event.type == pygame.KEYUP:
                    direction = (0, 0)
                if event.type == pygame.MOUSEBUTTONDOWN and game:
                    if event.button == 1:
                        delta1 = event.pos[0] - hero.rect.x
                        delta2 = event.pos[1] - hero.rect.y
                        d = round(hypot(delta1, delta2))
                        delta_x = 10 * delta1 / d
                        delta_y = 10 * delta2 / d

                        Ball2(hero.rect.x + 20, hero.rect.y - 10, delta_x, delta_y)

            if 0 < hero.rect.x + direction[0] <= 740:
                hero.rect.x += direction[0]
            if 0 < hero.rect.y + direction[1] <= 524:
                hero.rect.y += direction[1]
            if pygame.sprite.collide_mask(hero, boss):
                direction = (0, 0)
                health_1 -= 1
                hero.rect.x = 350
                hero.rect.y = 500

            delta_boss_bullet -= 1
            if not delta_boss_bullet and game:
                delta_boss_bullet = 20
                if boss_view == 1:
                    delta1 = hero.rect.x + 10 - (boss.rect.x + 20)
                    delta2 = hero.rect.y - 10 - (boss.rect.y + 220)
                else:
                    delta1 = hero.rect.x + 10 - (boss.rect.x + 150)
                    delta2 = hero.rect.y - 10 - (boss.rect.y + 220)
                d = round(hypot(delta1, delta2))
                delta_x = 5 * delta1 / d
                delta_y = 5 * delta2 / d
                if boss_view == 1:
                    Ball1(boss.rect.x + 20, boss.rect.y + 220, delta_x, delta_y)
                else:
                    Ball1(boss.rect.x + 150, boss.rect.y + 220, delta_x, delta_y)

            if boss.rect.y in (1, 10):
                boss_delta *= -1
            if boss.rect.x in (50, 600):
                boss_delta_2 *= -1
            boss.rect.x += boss_delta_2
            boss.rect.y += boss_delta
            count_boss_delta -= 1
            if count_boss_delta == 0:
                boss.rect.y += boss_delta
                count_boss_delta = 5
            if boss.rect.x > hero.rect.x and boss_view == 1:
                boss_view = 2
                im = pygame.transform.flip(boss.image, True, False)
                boss.image = im
            if boss.rect.x < hero.rect.x and boss_view == 2:
                boss_view = 1
                im = pygame.transform.flip(boss.image, True, False)
                boss.image = im
            #  старт отрисовки
            if pygame.mouse.get_focused():
                fon.draw(screen)
                if game:
                    bullets.update()
                    bullets.draw(screen)
                all_sprites.update()
                all_sprites.draw(screen)
                draw_health()
                pygame.draw.rect(screen, Color('black'), (550, 5, 210, 30))
                pygame.draw.rect(screen, Color('red'), (555, 10, boss_health * 2, 20))
                cur_sprite.draw(screen)
            elif not pygame.mouse.get_focused():
                fon.draw(screen)
                if game:
                    bullets.update()
                    bullets.draw(screen)
                all_sprites.update()
                all_sprites.draw(screen)
                draw_health()
                pygame.draw.rect(screen, Color('black'), (550, 5, 210, 30))
                pygame.draw.rect(screen, Color('red'), (555, 10, boss_health * 2, 20))
            if not health_1 or not boss_health:
                new = pygame.sprite.Group()
                game = False
                fin = pygame.sprite.Sprite()
                if not health_1:
                    fin.image = load_image('defeat.png')
                    fin.rect = fin.image.get_rect()
                    fin.rect.x = 225
                    a = 'd'
                    fin.rect.y = 100
                if not boss_health:
                    fin.image = load_image('victory.png')
                    fin.rect = fin.image.get_rect()
                    a = 'v'
                    fin.rect.x = 100
                    fin.rect.y = 100
                new.add(fin)
                new.draw(screen)
                pygame.display.flip()
                time.sleep(1)
                running3 = False
            if a == 'd':
                stadia = 'main'
            if a == 'v':
                stadia = 'play'
            pygame.display.flip()
            clock.tick(fps)
            board.del_monster()
            pygame.mouse.set_visible(True)






