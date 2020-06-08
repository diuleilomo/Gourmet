from src.exceptions import UserError
from src.ingredient import Ingredient

class WeightIngredient(Ingredient):

    def __init__(self, id, name, kind, stock, sWeight, mWeight, lWeight, sPrice, mPrice, lPrice):
        super().__init__(id, name, kind, stock)
        self._sWeight = sWeight
        self._mWeight = mWeight
        self._lWeight = lWeight
        self._sPrice = sPrice
        self._mPrice = mPrice
        self._lPrice = lPrice
    

    @property
    def sWeight(self):
        return self._sWeight

    @property
    def mWeight(self):
        return self._mWeight

    @property
    def lWeight(self):
        return self._lWeight

    @property
    def sPrice(self):
        return self._sPrice

    @property
    def mPrice(self):
        return self._mPrice

    @property
    def lPrice(self):
        return self._lPrice

    def __str__(self):
        return super().__str__() + f' | S-Weight: {self.sWeight} | M-Weight: {self.mWeight} | L-Weight: {self.lWeight}' \
        + f'| S-Price: ${self.sPrice} | M-Price: ${self.mPrice:.2f} | L-Price: ${self.lPrice:.2f}\n'
