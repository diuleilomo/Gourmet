from src.main import Main
from src.exceptions import DevError, StockError, UserError
from src.weightIngredient import WeightIngredient
from src.quantityIngredient import QuantityIngredient

class Order():

    def __init__(self, orderID):
        self._orderID = orderID
        self._status = None
        self._mains = []
        self._sideDrinks = []
        self._price = 0.00
        self._price_mains = 0.00
        self._price_sides = 0.00
        self._price_drinks = 0.00

    @property
    def orderID(self):
        return self._orderID

    @property
    def status(self):
        return self._status

    @property
    def mains(self):
        return self._mains

    @property
    def sideDrinks(self):
        return self._sideDrinks

    @property
    def price(self):
        return self._price

    @property
    def price_mains(self):
        return self._price_mains

    @property
    def price_sides(self):
        return self._price_sides

    @property
    def price_drinks(self):
        return self._price_drinks
    
    
    def add_main(self, type):
        if type == 'burger':
            main = Main('burger')
            self._mains.append(main)
            return main
        elif type == 'wrap':
            main = Main('wrap')
            self._mains.append(main)
            return main
        else:
            raise DevError('type should be either "burger" or "wrap"')

    def del_main(self, main):
        for target in self._mains:
            if main == target:
                main.remAllIngredients()    
                self._mains.remove(target)
                return 
    
        raise DevError("main that you're trying to delete doesn't exist in this order")

    def add_sideDrink(self, ingredient, amount, size):
        weight = None
        if isinstance(ingredient, WeightIngredient):
            weight = self.getWeight(ingredient, size)
        
        if self.isValidSideDrink(ingredient, amount, weight):
            self.addFoodToList(self._sideDrinks, ingredient, amount, size, weight)

    def del_sideDrink(self, ingredient, amount, size):
        if self._sideDrinks == None or self._sideDrinks == []:
            raise UserError(f"You don't have any sides or drinks in your order to remove.")
        self.removeFoodFromList(self._sideDrinks, ingredient, amount, size)

    def isValidSideDrink(self, ingredient, amount, weight):
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
         
    def change_status(self, status):
        if status != 'cooking' and status != 'ready for pickup':
            raise DevError('status should be either "cooking" or "ready for pickup"')
        self._status = status

    def calc_price(self):
        price = 0.00
        self._price = 0.00
        price += self.calc_price_mains()
        price += self.calc_price_sides()
        price += self.calc_price_drinks()
        price = round(price,2)
        self._price = price
        return price

    def calc_price_mains(self):
        price = 0.00
        self.Price_mains = 0.00
        for main in self._mains:
            price += main.price
        price = round(price,2)
        self._price_mains = price
        return price

    def calc_price_sides(self):
        price = 0.00
        self._price_sides = 0.00
        for sd in self._sideDrinks:
            if sd[0].kind == 's':
                if isinstance(sd[0], QuantityIngredient):
                    price += (sd[0].price * sd[1])
                elif sd[2] == 's':
                    price += (sd[0].sPrice * sd[1])
                elif sd[2] == 'm':
                    price += (sd[0].mPrice * sd[1])
                elif sd[2] == 'l':
                    price += (sd[0].lPrice * sd[1])
        price = round(price,2)
        self._price_sides = price
        return price

    def calc_price_drinks(self):
        price = 0.00
        self._price_drinks = 0.00
        for sd in self._sideDrinks:
            if sd[0].kind == 'd':
                if isinstance(sd[0], QuantityIngredient):
                    price += (sd[0].price * sd[1])
                elif sd[2] == 's':
                    price += (sd[0].sPrice * sd[1])
                elif sd[2] == 'm':
                    price += (sd[0].mPrice * sd[1])
                elif sd[2] == 'l':
                    price += (sd[0].lPrice * sd[1])
        price = round(price,2)
        self._price_drinks = price
        return price

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

    def __str__(self):
        return f'OrderID: {self.orderID} Status: {self.status} Mains: {self.mains} Sidedrinks: {self.sideDrinks}\n'

    




