#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

class Vec2d:
    """Функции для работы с векторами"""

    def __init__(self, x, y, speed = (0, 0)):
        self.x = int(x)
        self.y = int(y)
        self.speed = speed

    def __add__(self, other):
        """Сумма"""
        if isinstance(other, type(self)):
            return type(self)(self.x + other.x, self.y + other.y, self.speed)
        # elif isinstance(other, type(tuple())):
        #     return type(self)(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        """Разность"""
        return type(self)(self.x - other.x, self.y - other.y, self.speed)

    def __mul__(self, k):
        """Умножение на скаляр"""
        return type(self)(k * self.x, k * self.y, self.speed)

    def scal_mul(self, k):
        # скаля умнож
        return sum(k * self.x, k * self.y)

    def __len__(self):
        """длина"""
        return (self.x**2 + self.y**2)**0.5

    def int_pair(self):
        """получить картеж целых чисел"""
        return int(self.x), int(self.y)


class Polyline:
    SCREEN_DIM = (800, 600)

    def __init__(self):
        """Cоздание оснвого экрана и полей"""

        pygame.init()
        self.gameDisplay = pygame.display.set_mode(self.SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

        self.steps = 35
        self.working = True
        self.objects = []
        self.show_help = False
        self.pause = True
        self.hue = 0
        self.color = pygame.Color(0)

    # Функции отрисовки
    def draw_points(self, objects, style="points", width=3, color=(255, 255, 255)):
        """Функция отрисовки точек на экране"""

        if style == "line":
            for p_n in range(-1, len(objects) - 1):
                pygame.draw.line(self.gameDisplay, color,
                                 (objects[p_n].x, objects[p_n].y),
                                 (objects[p_n + 1].x, objects[p_n + 1].y), width)
        elif style == "points":
            for p in objects:
                pygame.draw.circle(self.gameDisplay, color,
                                   (p.x, p.y), width)

    def draw_help(self):
        """функция отрисовки экрана справки программы"""

        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "self.pause/Play"])
        data.append(["Num+", "More self.points"])
        data.append(["Num-", "Less self.points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current self.points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def set_points(self):
        """функция перерасчета координат опорных точек"""

        for p in range(len(self.objects)):
            curr_point = self.objects[p]
            curr_point.x = curr_point.x + curr_point.speed[0]
            curr_point.y = curr_point.y + curr_point.speed[1]

            if curr_point.x > self.SCREEN_DIM[0] or curr_point.x < 0:
                curr_point.speed = (- curr_point.speed[0], curr_point.speed[1])
            if curr_point.y > self.SCREEN_DIM[1] or curr_point.y < 0:
                curr_point.speed = (curr_point.speed[0], -curr_point.speed[1])

    def hanle_events(self):
        """События клавиш"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.working = False
                if event.key == pygame.K_r:
                    self.points = []
                    self.speeds = []
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                if event.key == pygame.K_KP_PLUS:
                    self.steps += 1
                if event.key == pygame.K_F1:
                    self.show_help = not self.show_help
                if event.key == pygame.K_KP_MINUS:
                    self.steps -= 1 if self.steps > 1 else 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                speed = (random.random() * 2, random.random() * 2)
                p = Vec2d(*event.pos, speed)
                self.objects.append(p)

    def render_screen(self):
        """Отрисовка тчек на экрана"""

        self.gameDisplay.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        self.draw_points(self.objects)
        self.handle_pause()

    def draw_line(self):
        """Соездинение точек прямыми"""

        self.draw_points(self.objects, style="line", width=3, color=(255, 255, 255))

    def handle_pause(self):
        """События паузы"""

        if not self.pause:
            self.set_points()
        if self.show_help:
            self.draw_help()
            print('help')

    # Основная программа
    def main_loop(self):
        """Основной цикл"""

        while self.working:
            self.hanle_events()
            self.render_screen()
            self.draw_line()
            pygame.display.flip()

class Knot(Polyline):
    """Сглаживание ломанной"""

    def get_point(self, list_base_points, alpha, deg=None):
        if deg is None:
            deg = len(list_base_points) - 1
        if deg == 0:
            return list_base_points[0]
        return list_base_points[deg]*alpha + self.get_point(list_base_points, alpha, deg - 1)*(1 - alpha)

    def get_points(self, list_base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(list_base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.objects) < 3:
            return []
        res = []
        for i in range(-2, len(self.objects) - 2):
            ptn = []
            new_point_left = (self.objects[i] + self.objects[i + 1]) * 0.5
            new_point_midle = self.objects[i + 1]
            new_point_right =  (self.objects[i+1] + self.objects[i + 2]) * 0.5
            ptn.append(new_point_left)
            ptn.append(new_point_midle)
            ptn.append(new_point_right)
            res.extend(self.get_points(ptn, count))
        return res

    def render_screen(self):
        """Соединение точек плавными киривыми"""

        super().render_screen()
        self.draw_points(self.get_knot(self.steps), "line", 3, self.color)

    def draw_line(self):
        pass

if __name__ == "__main__":
    m = Knot()
    m.main_loop()