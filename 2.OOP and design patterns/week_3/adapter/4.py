# from abc import ABC, abstractmethod
#
# class Light:
#     def __init__(self, dim):
#         # кортеж размер поля
#         self.dim = dim
#         # поле заданного размера
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
#         self.lights = []
#         self.obstacles = []
#
#     def set_dim(self, dim):
#         self.dim = dim
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
#
#     def set_lights(self, lights):
#         # устанавливает массив источников света с заданными координатами и просчитывает освещени
#         self.lights = lights
#         self.generate_lights()
#
#     def set_obstacles(self, obstacles):
#         # устанавливает препятствия аналогичным образом
#         self.obstacles = obstacles
#         self.generate_lights()
#
#     def generate_lights(self):
#         return self.grid.copy()
#
#
# class System:
#     def __init__(self):
#         self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
#         self.map[5][7] = 1  # Источники света
#         self.map[5][2] = -1  # Стены
#
#     def get_lightening(self, light_mapper):
#         self.lightmap = light_mapper.lighten(self.map)
#
#
# class AbstractAdapter(ABC):
#     @abstractmethod
#     def lighten(self, map):
#         pass

class MappingAdapter():
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def get_elements(self, grid):
        lights = []
        obstacles = []
        for i, row in enumerate(grid):
            for j, elem in enumerate(row):
                if elem == 1:
                    lights = lights + [(j, i)]
                if elem == -1:
                    obstacles = obstacles + [(j, i)]
        return lights, obstacles

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        lights, obstacles = self.get_elements(grid)
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)