import pytest

from src.quantityIngredient import QuantityIngredient, IngUserError
from src.weightIngredient import WeightIngredient
from src.system import System, UserError
from src.exceptions import DevError

# UC9 - new ingredients

def test_new_quantity_ingredient():
    food = QuantityIngredient(1, 'sesame bun', 'm', 20, 5.00)
    assert food.id == 1
    assert food.name == 'sesame bun'
    assert food.kind == 'm'
    assert food.stock == 20
    assert food.price == 5.00

def test_new_weight_ingredient():
    food = WeightIngredient(2, 'fries', 's', 2000, 60, 100, 140, 2, 2.8, 3.4)
    assert food.id == 2
    assert food.name == 'fries'
    assert food.kind == 's'
    assert food.stock == 2000
    assert food.sWeight == 60
    assert food.mWeight == 100
    assert food.lWeight == 140
    assert food.sPrice == 2.00
    assert food.mPrice == 2.80
    assert food.lPrice == 3.4

#UC9 - add ingredients

def test_addQuantityIngredient_correct_input():
    sys = System()
    sys.addQuantityIngredient('bun','m',20, 5)
    new=sys.ingredients[0]
    assert new.id == 1
    assert new.name == 'bun'
    assert new.kind == 'm'
    assert new.stock == 20
    assert new.price == 5

def test_addQuantityIngredient_wrong_name():
    sys=System()
    with pytest.raises(UserError) as error:
        sys.addQuantityIngredient(465,'m',20,5)   
    assert 'Name of ingredient must be in alphabets' in str(error.value)

def test_addQuantityIngredient_stock_is_string():
    sys=System()
    with pytest.raises(UserError) as error:
        sys.addQuantityIngredient('sugar','m','unsw', 5)   
    assert 'Stock of ingredient must be in number' in str(error.value)

def test_addQuantityIngredient_stock_is_negative():
    sys = System()
    with pytest.raises(UserError) as error:
        sys.addQuantityIngredient('sugar','s', -20 , 3)   
    assert 'Stock of ingredient must be positive' in str(error.value)

def test_addQuantityIngredient_price_is_string():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addQuantityIngredient('sesame bun','m' ,20, 'asdf')
    assert 'Price of ingredient must be a number' in str(e.value)
    
def test_addQuantityIngredient_price_is_negative():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addQuantityIngredient('sesame bun', 'm',20, -5)
    assert 'Price of ingredient must be positive' in str(e.value)

def test_addWeightIngredient_correct_input():
    sys = System()
    sys.addWeightIngredient('fries', 's', 2000, 60, 100, 140, 2, 2.8, 3.4)
    new = sys.ingredients[0]
    assert new.id == 2
    assert new.name == 'fries'
    assert new.kind == 's'
    assert new.stock == 2000
    assert new.sWeight == 60
    assert new.mWeight == 100
    assert new.lWeight == 140
    assert new.sPrice == 2
    assert new.mPrice == 2.8
    assert new.lPrice == 3.4

def test_addWeightIngredient_stock_is_string():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addWeightIngredient('ranch sauce','m' ,'one hundred', 2, 3, 4, 5, 5, 4)
    assert 'Stock of ingredient must be in number' in str(e.value)

def test_addWeightIngredient_stock_is_negative():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addWeightIngredient('fries', 'm' ,-1000, 60, 100, 140, 2, 2.8, 3.4)
    assert 'Stock of ingredient must be equal to or larger than 0' in str(e.value)

def test_addWeightIngredient_weight_is_string():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addWeightIngredient('fries','m' , 1000,'ewf', 'ewf', 'wef', 2.8, 3.4, 3.8)
    assert 'All weights of ingredient must be in number' in str(e.value)

def test_addWeightIngredient_weight_is_negative():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addWeightIngredient('fries', 'm' ,1000, -70, -90, -120, 4, 3, 1)
    assert 'All weights of ingredient must be larger than zero' in str(e.value)

def test_addWeightIngredient_price_is_string():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addWeightIngredient('fries','m' ,1000,152,400,600,'f','g','h')
    assert 'All prices of ingredient must be in number' in str(e.value)

def test_addWeightIngredient_price_is_negative():
    sys = System()
    with pytest.raises(UserError) as e:
        sys.addWeightIngredient('fries','m' ,100,70,90,120,-4,-3,-1)
    assert 'All prices of ingredient must be positive' in str(e.value)

# UC9 - remove ingredients

def test_remIngredient_correctinput():
    sys = System()
    sys.addQuantityIngredient('sesame bun', 'm' ,20, 1.00)
    sys.addWeightIngredient('fries','m' , 2000, 60, 100, 140, 2, 2.8, 3.4)
    sys.remIngredient(4)
    assert len(sys.ingredients) == 1
    assert sys.ingredients[0].name == 'sesame bun'

def test_remIngredient_incorrectinput():
    sys = System()
    sys.addQuantityIngredient('sesame bun', 'm' ,20, 1.00)
    with pytest.raises(DevError) as err:
        sys.remIngredient(1)
    assert 'cannot delete. no such ingredient in the inventory' in str(err.value)


# UC10 - update stock

def test_updateStock_valid_input():
    food = QuantityIngredient(1, 'sesame bun','m', 20, 5.00)
    food.updateStock(1000)
    assert food.stock == 1000

def test_updateStock_negative_num():
    food = QuantityIngredient(1, 'sesame bun', 'm', 20, 5.00)
    with pytest.raises(IngUserError) as error:
        food.updateStock(-35)
    assert 'Entry must be a positive number' in str(error.value)

def test_updateStock_float():
    food = QuantityIngredient(1, 'sesame bun', 'm', 20, 5.00)
    with pytest.raises(IngUserError) as error:
        food.updateStock(53.25)
    assert 'Entry must be an integer' in str(error.value)

def test_updateStock_string():
    food = QuantityIngredient(1, 'sesame bun', 'm', 20, 5.00)
    with pytest.raises(IngUserError) as error:
        food.updateStock('ten')
    assert 'Entry must be an integer' in str(error.value)