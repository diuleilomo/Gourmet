from abc import ABC, abstractmethod

class Ingredient(ABC):

    @abstractmethod
    def __init__(self, id, name, kind, stock):
        self._id = id
        self._name = name
        self._kind = kind
        self._stock = stock

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        self._stock = stock

    # amount is set as the new stock number
    # amount is valid when it is a positive integer
    def updateStock(self, amount):
        if not isinstance(amount, int):
            raise IngUserError('Entry must be an integer')
        elif amount < 0:
            raise IngUserError('Entry must be a positive number')
            
        self.stock = amount

    def __str__(self):
        return f"ID: {self.id} | Name: {self.name} |Kind: {self.kind} |Stock: {self.stock}"


class IngUserError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
