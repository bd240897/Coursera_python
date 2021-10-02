class MappingAdapter():
    def __init__(self, adaptee):
        self.adaptee = adaptee

    # def get_elements(self, grid):
    #     lights = []
    #     obstacles = []
    #     for i, row in enumerate(grid):
    #         for j, elem in enumerate(row):
    #             if elem == 1:
    #                 lights = lights + [(j, i)]
    #             if elem == -1:
    #                 obstacles = obstacles + [(j, i)]
    #     return lights, obstacles

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        obst = []
        lght = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                if grid[j][i] == 1:
                    lght.append((i, j))
                elif grid[j][i] == -1:
                    obst.append((i, j))
        self.adaptee.set_lights(lght)
        self.adaptee.set_obstacles(obst)
        return self.adaptee.grid