import Service

### паттерн НАБЛЮДАТЕЛЬ
class GameEngine:
    """Игровой движок - реализует паттерн НАБЛЮДАТЕЛЬ и хранит основную информации об игре"""
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0. # полученные очки
    game_process = True
    show_help = False

    def subscribe(self, obj): # подписываем окно на обновления движка
        """Подписать объект"""
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        """Удалить объект"""
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        """Отправить сообщение объекту - обновить его"""
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        """Cоздать героя"""
        self.hero = hero

    def interact(self):
        """Взаимодействие с объектами"""
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # MOVEMENT
    def move_up(self):
        """Движение героя вверх"""
        self.score -= 0.02 # уменьшение ОЧКОВ при хождении героя
        if self.map[self.hero.position[1] - 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] -= 1
        self.interact()

    def move_down(self):
        """Движение героя вниз"""
        self.score -= 0.02
        if self.map[self.hero.position[1] + 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] += 1
        self.interact()

    def move_left(self):
        """Движение героя влево"""
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] - 1] == Service.wall:
            return
        self.hero.position[0] -= 1 # текущиее кординаты персанажа
        self.interact()

    def move_right(self):
        """Движение героя выправо"""
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] + 1] == Service.wall:
            return
        self.hero.position[0] += 1
        self.interact()

    # MAP
    def load_map(self, game_map):
        """Загрузить карту"""
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        """Добавить объект на карту"""
        self.objects.append(obj)

    def add_objects(self, objects):
        """Добавить объект на карту???"""
        self.objects.extend(objects) # extend добавить несколько элементов в список

    def delete_object(self, obj):
        """Удалить объект с карты"""
        self.objects.remove(obj)
