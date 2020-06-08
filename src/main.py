from src.ingredient import Ingredient
from src.quantityIngredient import QuantityIngredient
from src.weightIngredient import WeightIngredient
from src.exceptions import DevError, UserError, StockError

class Main():
    
    def __init__(self, type):
        self._ingredients = [] 
        self._price = 0
        self._nBun = 0
        self._nPatty = 0

        if type != 'burger' and type != 'wrap':
            raise DevError('type must be either "burger"/"wrap"')
        else:
            self._type = type
        

    @property
    def ingredients(self):
        return self._ingredients

    @property
    def price(self):
        return self._price

    @property
    def type(self):
        return self._type

    @property
    def nBun(self):
        return self._nBun

    @property
    def nPatty(self):
        return self._nPatty

    def addIngredient(self, ingredient, amount, size):
        weight = None
        if isinstance(ingredient, WeightIngredient):
            weight = self.getWeight(ingredient, size)

        if self.isValid(ingredient, amount, weight) == True:
            self.addFoodToList(self._ingredients, ingredient, amount, size, weight)
            
            if 'bun' in ingredient.name:
                self._nBun += amount
            elif 'patty' in ingredient.name:
                self._nPatty += amount
            self.calcPrice()
                
    def remIngredient(self, ingredient, amount, size):
        if self._ingredients == None or self._ingredients == []:
            raise UserError(f"You don't have any ingredients in your main to remove.")
        self.removeFoodFromList(self._ingredients, ingredient, amount, size)
        self.calcPrice()

    # called only when deleting an entire main
    def remAllIngredients(self):
        for i in self._ingredients:
            if isinstance(i[0], QuantityIngredient):
                i[0].updateStock(i[0].stock + i[1])
            else:
                weight = self.getWeight(i[0], i[2])
                i[0].updateStock(i[0].stock + (i[1] * weight))
            self._ingredients.remove(i)
        
    #checks if amount of ingredients is valid to be sold
    def isValid(self, ingredient, amount, weight):
        # check buns
        if 'bun' in ingredient.name:
            if amount + self._nBun > 3:
                raise UserError(f"You can't add more than 3 buns to your order")
            if self._type == 'wrap':
                    raise UserError(f"You can't add a bun to a wrap")

        # check patties
        if 'patty' in ingredient.name:
            if amount + self._nPatty > 4:
                raise UserError(f"You can't add more than 4 patties to your order")
            
        # check stock
        if isinstance(ingredient, QuantityIngredient):
            if ingredient.stock >= amount:
                return True
            else:
                raise StockError(ingredient)
        else:
            if ingredient.stock > (amount * weight):
                return True
            else: 
                raise StockError(ingredient)

    # this method should be run when the main is completed
    # add to user interface
    def checkBurger(self):
        # check min buns
        if self._nBun < 2:
            raise UserError(f'You must finish your burger before moving on. It needs at least 2 buns to be finished.')
        else:
            return True

    def calcPrice(self):
        self._price = 0
        #base price
        if self.type == 'burger':
            self._price += 3
        else:
            self._price += 3.5
        #add ingredients
        for item in self._ingredients:
            if isinstance(item[0], QuantityIngredient):
                self._price += item[0].price * item[1]
            else: #is weightIngredient
                if item[2] == 's':
                    self._price += item[0].sPrice
                elif item[2] == 'm':
                    self._price += item[0].mPrice
                elif item[2] == 'l':
                    self._price +=item[0].lPrice
                else:
                    raise DevError('Invalid weight: must be s/m/l')

    def addFoodToList(self, list, ingredient, amount, size, weight):
        found = False
        for i in list:
            if i[0] == ingredient and i[2] == size:
                i[1] += amount
                found = True
                break
        if not found:
            list.append([ingredient, amount, size])
        
        if isinstance(ingredient, QuantityIngredient):
            ingredient.updateStock(ingredient.stock - amount)
        else:
            ingredient.updateStock(ingredient.stock - (amount * weight))

    def removeFoodFromList(self, list, ingredient, amount, size):
        for i in list:
            if i[0] == ingredient and i[2] == size:
                if i[1] >= amount:
                    i[1] -= amount
                    if isinstance(i[0], QuantityIngredient):
                        i[0].updateStock(i[0].stock + amount)
                    else:
                        weight = self.getWeight(ingredient, size)
                        i[0].updateStock(i[0].stock + (amount * weight))
                    if i[1] == 0:
                        list.remove(i)
                    return
                elif isinstance(ingredient, QuantityIngredient):
                    raise UserError(f"You don't have that many {ingredient.name} in your order to remove.")
                else:
                    raise UserError(f"You don't have that many {size} {ingredient.name} in your order to remove.")
        if isinstance(ingredient, QuantityIngredient):
            raise UserError(f"You don't have any {ingredient.name} in your order to remove.")
        else:
            raise UserError(f"You don't have any {size} {ingredient.name} in your order to remove.")

    def getWeight(self, ingredient, size):
        if size == 's':
            return ingredient.sWeight
        elif size == 'm':
            return ingredient.mWeight
        else: 
            return ingredient.lWeight



                
                