#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Функции для работы с векторами
# =======================================================================================
class Point:
    def __init__(self, x, y, speed = (0,0)):
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
        return sum(k * self.x, k * self.y, self.speed)

    def __len__(self):
        """длина"""
        return (self.x**2 + self.y**2)**0.5

    def int_pair(self):
        """получить картеж целых чисел"""
        return int(self.x), int(self.y)

class Main():
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

        self.steps = 35
        self.working = True
        self.objects = []
        self.show_help = False
        self.pause = True
        self.hue = 0
        self.color = pygame.Color(0)

    def sub(self, x, y):
        """"возвращает разность двух векторов"""
        return x[0] - y[0], x[1] - y[1]
    
    
    def add(self, x, y):
        """возвращает сумму двух векторов"""
        return x[0] + y[0], x[1] + y[1]
    
    
    def length(self, x):
        """возвращает длину вектора"""
        return math.sqrt(x[0] * x[0] + x[1] * x[1])
    
    
    def mul(self, v, k):
        """возвращает произведение вектора на число"""
        return v[0] * k, v[1] * k
    
    
    def vec(self, x, y):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return self, self.sub(y, x)


# =======================================================================================
# Функции отрисовки
# =======================================================================================
    def draw_points(self, objects, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
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


    # # =======================================================================================
    # # Функции, отвечающие за расчет сглаживания ломаной
    # # =======================================================================================
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
    #
    #
    def get_knot(self, objects, count):
        if len(objects) < 3:
            return []
        res = []
        for i in range(-2, len(self.objects) - 2):
            ptn = []
            new_point_left = self.objects[i] + self.objects[i + 1]
            new_point_left *= 0.5
            new_point_midle = self.objects[i + 1]
            new_point_right =  self.objects[i+1] + self.objects[i + 2]
            new_point_right *= 0.5
            ptn.append(new_point_left)
            ptn.append(new_point_midle)
            ptn.append(new_point_right)
            res.extend(self.get_points(ptn, count))
        return res
    #
    #
    def set_points(self, object):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.objects)):
            curr_point = self.objects[p]
            curr_point.x = curr_point.x + curr_point.speed[0]
            curr_point.y = curr_point.y + curr_point.speed[1]

            if curr_point.x > SCREEN_DIM[0] or curr_point.x < 0:
                curr_point.speed = (- curr_point.speed[0], curr_point.speed[1])
            if curr_point.y > SCREEN_DIM[1] or curr_point.y < 0:
                curr_point.speed = (curr_point.speed[0], -curr_point.speed[1])
# =======================================================================================
# Основная программа
# =======================================================================================

    def main_loop(self):
        while self.working:
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
                    p = Point(*event.pos, speed)
                    self.objects.append(p)

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            self.draw_points(self.objects)
            self.draw_points(self.get_knot(self.objects, self.steps), "line", 3, self.color)
            if not self.pause:
                self.set_points(self.objects)
            if self.show_help:
                self.draw_help()
                print('help')

            pygame.display.flip()
        # pygame.display.quit()
        # pygame.quit()
        # exit(0)




class Polyline:
    """Класс замкнутых ломаных"""
    def __init__(self):
        self.points = list()

    def add_point(self, point):
        self.points.append(point)

    def delete_point(self, point=None):
        if point is None:
            self.points.pop()
        else:
            self.points.remove(point)

    def set_points(self):
        _width = SCREEN_DIM[0]
        _height = SCREEN_DIM[1]
        for p in range(len(self.points)):
            self.points[p] = self.points[p] * self.points[p].speed

            if self.points[p][0] > _width or self.points[p][0] < 0:
                self.points[p].speed = (- self.points[p].speed[0],
                                        self.points[p].speed[1])

            if self.points[p][1] > _height or self.points[p][1] < 0:
                self.points[p].speed = (self.points[p].speed[0],
                                        -self.points[p].speed[1])

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for point in points:
            pygame.draw.circle(self.gameDisplay, color, point.int_pair(), width)

class Knot(Polyline):
    # Сглаживание ломаной
    Knots = []

    def __init__(self, count):
        super().__init__()
        self.count = count
        Knot.Knots.append(self)

    def add_point(self, point):
        super().add_point(point)
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def delete_point(self, point=None):
        super().delete_point(point)
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha,
                                                    deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [(self.points[i] + self.points[i + 1]) * HALF,
                   self.points[i + 1],
                   (self.points[i + 1] + self.points[i + 2]) * HALF]
            res.extend(self.get_points(ptn))
        return res

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             points[p].int_pair(),
                             points[p + 1].int_pair(), width)

if __name__ == "__main__":
    m = Main()
    m.main_loop()