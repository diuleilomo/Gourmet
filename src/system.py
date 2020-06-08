from src.order import Order
from src.exceptions import UserError, DevError 
from src.main import Main
from src.ingredient import Ingredient
from src.quantityIngredient import QuantityIngredient
from src.weightIngredient import WeightIngredient

newID = 0

class System():

    
    def __init__(self):
        self._orders = []
        self._ingredients = []
        self._currOrder = Order(0)
   
    @property
    def ingredients(self):
        return self._ingredients
    
    @property
    def orders(self):
        return self._orders

    @property
    def currOrder(self):
        return self._currOrder

    def newOrder(self):
        if not self._orders:
            order = Order(0)
            self._orders.append(order)
            self._currOrder = order
        else:
            order = Order(len(self._orders))
            self._orders.append(order)
            self._currOrder = order
        return order

    def deleteOrder(self,id):
        for o in self._orders:
            if o.orderID ==id:
                self._orders.remove(o)

    def checkoutOrder(self, order):
        order.calc_price()
        self.payForOrder(order)
        # print(self._orders[i].price)
        self.updateOrderStatus(order.orderID, 'cooking')
        return order.price

    def payForOrder(self, order):
        print(f'You have successfully paid for your order. Your Order ID is: {order.orderID}')
            
    def updateOrderStatus(self, id, status):
        for o in self._orders:
            if o.orderID == id:
                o.change_status(status)

    def checkOrderStatus(self, id):
        for o in self._orders:
            if o.orderID == id:
                return o.status

    def ordersOverview(self):
        return self._orders

    def viewOrder(self, order):
        print(order)

    def searchOrder(self, id):
        for o in self._orders:
            if o.orderID == id:
                return o
        raise UserError('OrderID not exist in the system')

    def ingredientsOverview(self):
        return self._ingredients

    def addQuantityIngredient(self, name, kind, stock, price):
        if not isinstance(name, str):
            raise UserError('Name of ingredient must be in alphabets')
        if kind != 'm' and kind != 'd' and kind != 's':
            raise DevError('kind must be either "m"/"s"/"d"')
        if not isinstance(stock, int):
            raise UserError('Stock of ingredient must be in number')
        if float(stock) < 0:
            raise UserError('Stock of ingredient must be positive')
        if not isinstance(price, float) and not isinstance(price, int):
            raise UserError('Price of ingredient must be a number')
        if float(price) < 0:
            raise UserError('Price of ingredient must be positive')
        
        global newID
        newID += 1
        new = QuantityIngredient(newID, name, kind, stock, price) 
        self._ingredients.append(new)  


    def addWeightIngredient(self, name, kind, stock, sWeight, mWeight, lWeight, sPrice, mPrice, lPrice):
        if not isinstance(name, str):
            raise UserError('Name of ingredient must be in alphabets')
        if kind != 'm' and kind != 'd' and kind != 's':
            raise DevError('kind must be either "m"/"s"/"d"')
        if not isinstance(stock, int):
            raise UserError('Stock of ingredient must be in number')
        if int(stock) < 0:
            raise UserError('Stock of ingredient must be equal to or larger than 0')
        if not isinstance(sWeight, int) or not isinstance(mWeight, int) or not isinstance(lWeight, int):
            raise UserError('All weights of ingredient must be in number')
        if int(sWeight) <= 0 or int(mWeight) <= 0 or int(lWeight) <= 0:
            raise UserError('All weights of ingredient must be larger than zero')
        if isinstance(sPrice, str) or isinstance(mPrice, str) or isinstance(lPrice, str):
            raise UserError('All prices of ingredient must be in number')
        if not isinstance(float(sPrice), float) or not isinstance(float(mPrice), float) or not isinstance(float(lPrice), float):
            raise UserError('All prices of ingredient must be in number')
        if float(sPrice) < 0 or float(mPrice) < 0 or float(lWeight) < 0:
            raise UserError('All prices of ingredient must be positive')
        
        global newID
        newID += 1
        new = WeightIngredient(newID, name, kind, stock, sWeight, mWeight, lWeight, sPrice, mPrice, lPrice)
        self._ingredients.append(new)  
        
    def remIngredient(self, id):
        for i in self._ingredients:
            if i.id == id:
                self._ingredients.remove(i)
                return
                
        raise DevError('cannot delete. no such ingredient in the inventory')

    def updateStock(self, id, amount):
        for i in self._ingredients:
            if i.id == id:
                index = self._ingredients.index(i)
                self._ingredients[index].stock = amount
                return
                
        raise DevError("Ingredient not found, can't update")
        
    # def checkIngredients(self,ingredient):
    #     valid=1
    #     for i in self._ingredients:
    #         print(self._ingredients[i].name)
    #         if self._ingredients[i].name==ingredient.name:
    #             if self._ingredients[i].stock<ingredient[i].stock:
    #                 valid=0
    #     return valid
    
    
    
        
    
    