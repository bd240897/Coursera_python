from abc import ABC
class SomeObject:
    def __init__(self):
        self.integer_field = 4
        self.float_field = 1.9
        self.string_field = "sadsad"

class EventGet():
    def __init__(self, event_type):
        self.event_type = event_type


class EventSet():
    def __init__(self, event_type):
        self.event_type = event_type


class IntHandler():
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.event_type == int:
                return obj.integer_field
            else:
                return self.__successor.handle(obj, event)
        if isinstance(event, EventSet):
            if isinstance(event.event_type, int):
                obj.integer_field = event.event_type
            else:
                if self.__successor is not None:
                    self.__successor.handle(obj, event)

class FloatHandler():
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.event_type == float:
                return obj.float_field
            else:
                return self.__successor.handle(obj, event)
        if isinstance(event, EventSet):
            if isinstance(event.event_type, float):
                obj.float_field = event.event_type
            else:
                if self.__successor is not None:
                    self.__successor.handle(obj, event)

class StrHandler():
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.event_type == str:
                return obj.string_field
            else:
                return self.__successor.handle(obj, event)
        if isinstance(event, EventSet):
            if isinstance(event.event_type, str):
                obj.string_field = event.event_type
            else:
                if self.__successor is not None:
                    self.__successor.handle(obj, event)

chain = IntHandler(FloatHandler(StrHandler()))

obj = SomeObject()
chain.handle(obj, EventSet('job'))
chain.handle(obj, EventSet(911))
chain.handle(obj, EventSet(9.11))
print(obj.string_field)
print(obj.integer_field)
print(obj.float_field)
print(chain.handle(obj, EventGet(int)))
print(chain.handle(obj, EventGet(str)))
print(chain.handle(obj, EventGet(float)))