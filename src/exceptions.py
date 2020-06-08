from src.quantityIngredient import QuantityIngredient

class DevError(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class UserError(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class StockError(Exception):
    
    def __init__(self, ingredient):
        if isinstance(ingredient, QuantityIngredient):
            super().__init__(f"Not enough {ingredient.name} in stock: {ingredient.stock} left.")
        else:
            super().__init__(f"Not enough {ingredient.name} in stock: {ingredient.stock} gms/mls left.")