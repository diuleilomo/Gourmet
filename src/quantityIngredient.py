from src.ingredient import Ingredient, IngUserError

class QuantityIngredient(Ingredient):

    def __init__(self, id, name, kind, stock, price):
        super().__init__(id, name, kind, stock)
        self._price = price

    @property
    def price(self):
        return self._price

    def __str__(self):
        return super().__str__() + f'| Price: ${self.price:.2f}\n'
