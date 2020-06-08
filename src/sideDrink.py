class SideDrink():

    #ingredient should be of type: quantityIngredient/weightIngredient
    #size should be one of these: None/'s'/'m'/'l'
    #temp should be one of these: None/'h'/'c'
    def __init__(self, ingredient, size):
        self._ingredient = ingredient
        self._size = size

        #price setting
        if self.size == None:
            self._price = self.ingredient.price
        elif self.size == 's':
            self._price = self.ingredient.sPrice
        elif self.size == 'm':
            self._price = self.ingredient.mPrice
        elif self.size == 'l':
            self._price = self.ingredient.lPrice

    @property
    def ingredient(self):
        return self._ingredient

    @property
    def size(self):
        return self._size

    @property
    def price(self):
        return self._price

    def __str__(self):
        return f'Name: {self.ingredient.name} | Size: {self.size} | Price: ${self.price:.2f}\n'

