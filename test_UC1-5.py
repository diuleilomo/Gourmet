from src.system import System
from src.exceptions import DevError, UserError,StockError
from src.order import Order 
from src.main import Main
from src.ingredient import Ingredient
from src.quantityIngredient import QuantityIngredient
from src.weightIngredient import WeightIngredient

import pytest

#UC1-Create base main & UC2-Create custom main

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

def test_check_burger_valid():
    main = Main('burger')
    bun = QuantityIngredient(1, 'bun','m', 10, 1.5)
    main.addIngredient(bun, 2, None)
    assert main.checkBurger() == True
    
def test_check_burger_invalid():
    main = Main('burger')
    bun = QuantityIngredient(1, 'bun','m', 10, 1.5)
    main.addIngredient(bun, 1, None)
    with pytest.raises(UserError) as err:
        main.checkBurger()
    assert  "You must finish your burger before moving on. It needs at least 2 buns to be finished." in str(err.value)

def test_addIngredient_tomato_to_burger_enough_stock():
    main = Main('burger')
    tomato = QuantityIngredient(1, 'tomato', 'm', 20, 1)
    main.addIngredient(tomato, 5, None)
    assert main.ingredients[0][0] == tomato  
    assert main.ingredients[0][1] == 5
    assert main.price == 8
    assert main.nBun == 0
    assert main.nPatty == 0
    assert main.type == 'burger'

def test_addIngredient_tomato_to_burger_not_enough_stock():
    main = Main('burger')
    tomato = QuantityIngredient(1, 'tomato', 'm', 4, 0.2)
    with pytest.raises(StockError) as error: 
        main.addIngredient(tomato, 5, None)
    assert "Not enough tomato in stock: 4 left." in str(error.value)

def test_addIngredient_weightIngredient_to_burger():
    main = Main('wrap')
    lettuce = WeightIngredient(1, 'lettuce', 'm', 2000, 50, 100, 150, .50, 1, 1.5)
    main.addIngredient(lettuce, 1, 's')
    assert main.ingredients[0][0] == lettuce  
    assert main.ingredients[0][1] == 1
    assert main.ingredients[0][2] == 's'
    assert main.price == 4

def test_add_bun_to_burger_within_range():
    main = Main('burger')
    bun = QuantityIngredient(1, 'bun', 'm', 10, 1.5)
    main.addIngredient(bun, 3, None)
    assert main.ingredients[0][0] == bun 
    assert main.ingredients[0][1] == 3
    assert main.price == 7.5 
    assert main.nBun == 3
    assert main.nPatty == 0
    assert main.type == 'burger'
    
def test_add_bun_to_burger_too_many_buns():
    main = Main('burger')
    bun = QuantityIngredient(1, 'bun', 'm', 10, 1.5)
    with pytest.raises(UserError) as error: 
        main.addIngredient(bun, 4, None)
    assert "You can't add more than 3 buns to your order" in str(error.value)
      
def test_add_patty_to_burger_within_range():
    main=Main('burger')
    patty=QuantityIngredient(1, 'patty', 'm', 25, 5)
    main.addIngredient(patty, 3, None)
    assert main.ingredients[0][0] == patty
    assert main.ingredients[0][1] == 3
    assert main.price == 18 
    assert main.nBun == 0
    assert main.nPatty == 3
    assert main.type == 'burger'

def test_add_Patty_to_Burger_too_many_patties():
    main=Main('burger')
    patty=QuantityIngredient(1, 'patty', 'm', 25, 5)
    with pytest.raises(UserError) as error: 
        main.addIngredient(patty, 5, None)
    assert "You can't add more than 4 patties to your order" in str(error.value)

def test_addIngredient_add_bun_to_wrap():
    main = Main('wrap')
    bun = QuantityIngredient(0, 'bun', 'm', 20, .50)
    with pytest.raises(UserError) as error:
        main.addIngredient(bun, 2, None)
    assert "You can't add a bun to a wrap" in str(error.value)

def test_remIngredient_incorrect_input_no_ings_in_order():
    sys = System()
    wrap = Main('wrap')
    sys.addQuantityIngredient('beef patty', 'm', 50, 1.50)
    ing1 = sys.ingredients[0]

    with pytest.raises(UserError) as error:
        wrap.remIngredient(ing1, 1, None)
    assert "You don't have any ingredients in your main to remove." in str(error.value)

def test_remIngredient_incorrect_input():
    sys = System()
    sys.addQuantityIngredient('beef patty', 'm', 50, 1.50)
    sys.addQuantityIngredient('cheese', 'm', 50, 1.00)
    sys.addQuantityIngredient('egg', 'm', 50, 1.50)
    ing1 = sys.ingredients[0]
    ing2 = sys.ingredients[1]
    ing3 = sys.ingredients[2]

    wrap = Main('wrap')
    wrap.addIngredient(ing1, 2, None)
    wrap.addIngredient(ing2, 2, None)
    with pytest.raises(UserError) as error:
        wrap.remIngredient(ing3, 1, None)
    assert "You don't have any egg in your order to remove." in str(error.value)

def test_remIngredient_correct_input():
    sys = System()
    sys.addQuantityIngredient('beef patty', 'm', 50, 1.50)
    sys.addQuantityIngredient('cheese', 'm', 50, 1.00)
    sys.addQuantityIngredient('egg', 'm', 50, 1.50)
    ing1 = sys.ingredients[0]
    ing2 = sys.ingredients[1]
    ing3 = sys.ingredients[2]

    wrap = Main('wrap')
    wrap.addIngredient(ing1, 2, None)
    wrap.addIngredient(ing2, 2, None)
    wrap.addIngredient(ing3, 1, None)

    wrap.remIngredient(ing3, 1, None)
    assert len(wrap.ingredients) == 2
    assert sys.ingredients[2].stock == 50



#UC3-See price of main


def test_calc_price():
    order = Order(1)
    main = order.add_main('burger')
    ing1 = QuantityIngredient(1, 'sesame bun', 'm', 20, 1.00)
    main.addIngredient(ing1, 2, None)
    ing2 = WeightIngredient(2, 'fries', 's', 2000, 60, 100, 140, 2, 2.8, 3.4)
    order.add_sideDrink(ing2, 1, None)
    
    assert order.calc_price() == 5.0



#UC4-Order sides and drinks
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

#UC5-Checkout
    
def test_change_status_correct():
    order=Order(1)
    order.change_status('cooking')
    assert order.status=='cooking'

def test_change_status_incorrect():
    order = Order(1)
    with pytest.raises(DevError) as e:
        order.change_status('in jail')
    assert 'status should be either "cooking" or "ready for pickup"' in str(e.value)
