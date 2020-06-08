from src.system import System
from src.exceptions import UserError, DevError
from src.order import Order
from src.main import Main
from src.quantityIngredient import QuantityIngredient
from src.weightIngredient import WeightIngredient

import pytest

#UC6-check order status

def test_newOrder():
    sys = System()
    sys.newOrder()
    assert len(sys.orders) == 1
    assert sys.orders[0].orderID == 0

def test_checkoutorder():
    sys = System()
    order = sys.newOrder()
    price = sys.checkoutOrder(order)
    assert sys.checkOrderStatus(0) == 'cooking'
    assert price == order.price

def test_checkOrderStatus_blank():
    sys = System()
    sys.newOrder()
    assert sys.checkOrderStatus(0) == None
    

#UC7 - view orders
    
def test_orders_overview():
    sys = System()
    order1 = sys.newOrder()
    order2 = sys.newOrder()
    order3 = sys.newOrder()
    assert sys.ordersOverview() == [order1, order2, order3]
    
def test_search_order_correct_input():
    sys = System()
    order0 = sys.newOrder()
    order1 = sys.newOrder()
    order2 = sys.newOrder()
    assert sys.searchOrder(1) == order1

def test_search_order_incorrect_input():
    sys = System()
    order0 = sys.newOrder()
    order1 = sys.newOrder()
    order2 = sys.newOrder()
    
    with pytest.raises(UserError) as err:
        sys.searchOrder(32)
    assert 'OrderID not exist in the system' in str(err.value)

# UC7 - new orders / modify orders

def test_new_order():
    newOrder = Order(420)
    assert newOrder.orderID == 420
    assert newOrder.status == None
    assert not newOrder.mains    
    assert not newOrder.sideDrinks

def test_add_main_correct_input():
    order = Order(1)
    order.add_main('burger')
    order.add_main('wrap')
    assert order.mains[0].type == 'burger'
    assert order.mains[1].type == 'wrap'

def test_add_main_incorrect_type_of_Main():
    order = Order(1)
    with pytest.raises(DevError) as e:
        order.add_main('hamburger')
    assert 'type should be either "burger" or "wrap"' in str(e.value)

def test_del_main_correct_input():
    order = Order(1)
    main = order.add_main('burger')
    order.del_main(main)
    assert not order.mains
    
def test_del_main_incorrect_input():
    order = Order(1)
    order.add_main('burger')
    wrong_main = Main('wrap')
    with pytest.raises(DevError) as e:
        order.del_main(wrong_main)
    assert "main that you're trying to delete doesn't exist in this order" in str(e.value)

def test_add_sidedrink():
    order = Order(1)
    ing = WeightIngredient(2, 'fries', 's', 2000, 60, 100, 140, 2, 2.8, 3.4)
    order.add_sideDrink(ing, 2, 'l')
    assert order.sideDrinks[0][0] == ing
    assert order.sideDrinks[0][1] == 2
    assert order.sideDrinks[0][2] == 'l'

def test_del_sideDrinks_correct_input():
    order = Order(1)
    ing = WeightIngredient(2, 'fries', 's', 2000, 60, 100, 140, 2, 2.8, 3.4)
    order.add_sideDrink(ing, 2, 'l')
    order.del_sideDrink(ing, 2, 'l')
    assert not order.sideDrinks
  
def test_del_sideDrinks_incorrect_input():
    order = Order(1)
    ing = WeightIngredient(2, 'fries', 's', 2000, 60, 100, 140, 2, 2.8, 3.4)
    order.add_sideDrink(ing, 2, 'l')
    ing2 = QuantityIngredient(1, 'can of coke', 'd', 40, 3)
    with pytest.raises(UserError) as e:
        order.del_sideDrink(ing2, 1, 's')
    assert "You don't have any can of coke in your order to remove." in str(e.value)
    
# UC8 - update orders

def test_calc_price():
    order = Order(1)
    main = order.add_main('burger')
    ing1 = QuantityIngredient(1, 'sesame bun', 'm', 20, 1.00)
    main.addIngredient(ing1, 2, None)
    ing2 = WeightIngredient(2, 'fries', 's', 2000, 60, 100, 140, 2, 2.8, 3.4)
    order.add_sideDrink(ing2, 1, None)
    
    assert order.calc_price() == 5.0
    
def test_change_status_correct():
    order=Order(1)
    order.change_status('cooking')
    assert order.status=='cooking'

def test_change_status_incorrect():
    order = Order(1)
    with pytest.raises(DevError) as e:
        order.change_status('in jail')
    assert 'status should be either "cooking" or "ready for pickup"' in str(e.value)

def test_updateOrderStatus():
    sys = System()
    sys.newOrder()
    sys.updateOrderStatus(0, 'cooking')
    assert sys.checkOrderStatus(0) == 'cooking'
