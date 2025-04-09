from Exceptions import OwnEmpty
import json

class ArrayQueue:
    """Cola FIFO compatible con SQLAlchemy."""
    DEFAULT_CAPACITY = 10

    def __init__(self, initial_elements=None):
        self.data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self.size = 0
        self.front = 0
        if initial_elements:
            for element in initial_elements:
                self.enqueue(element)

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def first(self):
        if self.is_empty():
            raise OwnEmpty("Cola vacía")
        return self.data[self.front]

    def dequeue(self):
        if self.is_empty():
            raise OwnEmpty("Cola vacía")
        answer = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % len(self.data)
        self.size -= 1
        return answer

    def enqueue(self, e):
        if self.size == len(self.data):
            self.resize(2 * len(self.data))
        avail = (self.front + self.size) % len(self.data)
        self.data[avail] = e
        self.size += 1

    def resize(self, cap):
        old = self.data
        self.data = [None] * cap
        walk = self.front
        for k in range(self.size):
            self.data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self.front = 0

    def to_json(self):
        """Convierte la cola a una lista JSON para almacenar en BD."""
        elements = []
        walk = self.front
        for _ in range(self.size):
            elements.append(self.data[walk])
            walk = (walk + 1) % len(self.data)
        return json.dumps(elements)

    @classmethod
    def from_json(cls, json_str):
        """Crea una cola desde una cadena JSON (al cargar desde BD)."""
        elements = json.loads(json_str)
        return cls(elements)