from flask import render_template, request, redirect, url_for, abort
from server import app, system, main
from src.exceptions import StockError, UserError
from src.quantityIngredient import QuantityIngredient
from src.weightIngredient import WeightIngredient
from datetime import datetime
import pickle

'''
Custom filters
'''
@app.template_filter('isQIngredient')
def isQIngredient(x):
    return isinstance(x, QuantityIngredient)

@app.template_filter('isWIngredient')
def isWIngredient(x):
    return isinstance(x, WeightIngredient)

@app.template_filter('isNone')
def isNone(x):
    return x == None

'''
Dedicated page for "page not found"
'''
#@app.route('/404')
#@app.errorhandler(404)
#def page_not_found():
#    return render_template('404.html')


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/check_order', methods=['GET','POST'])
def check_order():
    if request.method == 'POST':
        orderID = int(request.form.get("orderID"))
        result = system.checkOrderStatus(orderID) 
        return render_template("view_check_order.html", result = result)
    return render_template("check_order.html")


@app.route('/view_ingredients', methods=["GET", "POST"])
def view_ingredients():
    if request.method == 'POST':
        if 'filter' in request.form:
            print("filter run")
            unk = request.form.get("filter")
            if unk == '':
                switch = ''
            elif unk == 'main':
                switch = 'main'
            elif unk == 'side':
                switch = 'side'
            elif unk == 'drink':
                switch = 'drink'

        if 'stock' in request.form:
            print("stock run")
            temp = str("new_stock" + request.form.get("stock"))
            print (temp)
            print (int(request.form.get("stock")))
            system.updateStock(int(request.form.get("stock")), int(request.form.get(temp)))

        if 'delete' in request.form:
            print("delete run")
            system.remIngredient(int(request.form.get("delete")))

        f = open("system.pickle", "wb")
        pickle.dump(system, f)

        return render_template("view_ingredients.html", ingredients = system.ingredientsOverview(), filter = switch)
  
    return render_template("view_ingredients.html", ingredients = system.ingredientsOverview(), filter = "")

@app.route('/add_ingredients', methods=["GET", "POST"])
def add_ingredients():
    if request.method == 'POST':
        if 'quantity' in request.form:
            name = request.form.get("name1")
            kind = request.form.get("kind1")
            stock = request.form.get("stock1")
            price = request.form.get("price")

            system.addQuantityIngredient(name, str(kind), int(stock), float(price))

        if 'weight' in request.form:
            name = request.form.get("name2")
            kind = request.form.get("kind2")
            stock = request.form.get("stock2")
            sWeight = request.form.get("sWeight")
            mWeight = request.form.get("mWeight")
            lWeight = request.form.get("lWeight")
            sPrice = request.form.get("sPrice")
            mPrice = request.form.get("mPrice")
            lPrice = request.form.get("lPrice")

            system.addWeightIngredient(name, str(kind), int(stock), int(sWeight), int(mWeight), int(lWeight), 
            float(sPrice), float(mPrice), float(lPrice))

        f = open("system.pickle", "wb")
        pickle.dump(system, f)

        return redirect(url_for('view_ingredients'))
        

    return render_template("add_ingredients.html")

@app.route('/new_order')
def new_order():
    system.newOrder()
    return render_template("new_order.html")

@app.route('/base_main', methods=["GET", "POST"])
def base_main():
    msg3 = "Your current order total is $"
    if request.method == 'POST':
        currOrder = system.currOrder
        ingredients = system.ingredients

        nBurger = request.form.get('burger')
        nWrap = request.form.get('wrap')
        if nBurger == '':
            nBurger = 0
        else:
            nBurger = int(nBurger)
        if nWrap == '':
            nWrap = 0
        else:
            nWrap = int(nWrap)
        if nBurger < 1 and nWrap < 1:
            price = currOrder.calc_price()
            msg3 += f"{price:.2f}"
            return render_template("base_main.html", msg1 = 'Please add a valid number of burgers or wraps to the order.', msg3 = msg3)
        else:
            main = None
            addedBurgers = 0
            addedWraps = 0
            try:
                for i in range(nBurger):
                    main = currOrder.add_main('burger')
                    for ing in ingredients:
                        if 'sesame bun' in ing.name:
                            main.addIngredient(ing, 2, None)
                        elif 'beef patty' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'cheese' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'egg' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'ketchup' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'lettuce' in ing.name:
                            main.addIngredient(ing, 1, 's')
                    # main.addIngredient(ingredients[0], 2, None) #sesame buns
                    # main.addIngredient(ingredients[2], 1, None) #beef patty
                    # main.addIngredient(ingredients[5], 1, None) #cheese
                    # main.addIngredient(ingredients[6], 1, None) #egg
                    # main.addIngredient(ingredients[7], 1, None) #ketchup
                    # main.addIngredient(ingredients[8], 1, 's') #lettuce
                    addedBurgers += 1
                for i in range(nWrap):
                    main = currOrder.add_main('wrap')
                    for ing in ingredients:
                        if 'schnitzel' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'cheese' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'egg' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'ketchup' in ing.name:
                            main.addIngredient(ing, 1, None)
                        elif 'lettuce' in ing.name:
                            main.addIngredient(ing, 1, 's')
                    # main.addIngredient(ingredients[4], 1, None) #schnitzel
                    # main.addIngredient(ingredients[5], 1, None) #cheese
                    # main.addIngredient(ingredients[6], 1, None) #egg
                    # main.addIngredient(ingredients[7], 1, None) #ketchup
                    # main.addIngredient(ingredients[8], 1, 's') #lettuce
                    addedWraps += 1
            except StockError as e:
                system.currOrder.del_main(main) #remove the main that didn't have enough stock to fulfil it
                price = currOrder.calc_price()
                msg3 += f"{price:.2f}"
                return render_template("base_main.html", msg1 = "We're sorry! We don't have enough stock to fulfil that order. " 
                + str(e), msg2 = f"\nSuccessfully added {addedBurgers} burgers & {addedWraps} wraps. ", msg3 = msg3)

            price = currOrder.calc_price()
            msg3 += f"{price:.2f}"
            return render_template("base_main.html", msg1 = f'Successfully added {addedBurgers} burgers & {addedWraps} wraps'
            , msg3 = msg3)
        
    return render_template("base_main.html")

@app.route('/custom_main', methods=["GET", "POST"])
def custom_main():
    global main
    if request.method == 'POST':
        if request.form.get('type') == 'Burger':
            main = None
            return redirect(url_for('custom_main_create', kind = 'burger'))
        else:
            main = None
            return redirect(url_for('custom_main_create', kind = 'wrap'))

    return render_template("custom_main.html")

@app.route('/custom_main_create/<kind>', methods=["GET", "POST"])
def custom_main_create(kind):
    msg1 = ''
    msg2 = ''
    msg3 = 'Your main so far: '
    msg4 = 'The price of this main so far is $'
    msg5 = 'Your current order total is $'
    msg6 = ''
    currOrder = system.currOrder
    ingredients = system.ingredients
    errors = []
    addsuccesses = []
    delsuccesses = []

    global main
    if main == None:
        if kind == 'burger':
            main = currOrder.add_main('burger')
        else: 
            main = currOrder.add_main('wrap')

    if request.method == 'POST':
        if 'add' in request.form:
            for i in ingredients:
                if i.kind == 'm':
                    if isQIngredient(i):
                        n = request.form.get(i.name)
                        if n != '':
                            n = int(n)
                            if n > 0:
                                try:
                                    main.addIngredient(i, n, None)
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, ''])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    main.remIngredient(i, n, None)
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, ''])

                    else: # isWIngredient
                        n = request.form.get('s' + i.name)
                        if n != '':
                            n = int(n)
                            if n > 0:
                                try:
                                    main.addIngredient(i, n, 's')
                                except StockError as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, 's'])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    main.remIngredient(i, n, 's')
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, 's'])

                        n = request.form.get('m' + i.name)
                        if n != '':
                            n = int(n)
                            if n > 0:
                                try:
                                    main.addIngredient(i, n, 'm')
                                except StockError as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, 'm'])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    main.remIngredient(i, n, 'm')
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, 'm'])

                        n = request.form.get('l' + i.name)
                        if n != '':
                            n = int(n)
                            if n > 0:
                                try:
                                    main.addIngredient(i, n, 'l')
                                except StockError as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, 'l'])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    main.remIngredient(i, n, 'l')
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, 'l'])

            if addsuccesses:
                msg1 = 'Successfully added '
                for s in addsuccesses:
                    msg1 += str(s[1]) + ' ' + s[2]  + ' ' + s[0] + ', '
                msg1 += ' to your main.'
            
            if delsuccesses:
                msg6 = 'Successfully removed '
                for s in delsuccesses:
                    msg6 += str(s[1]) + ' ' + s[2]  + ' ' + s[0] + ', '
                msg6 += ' from your main.'

            if errors:
                for e in errors:
                    msg2 += str(e)
                    msg2 += ' '

            for i in main.ingredients:
                if isQIngredient(i[0]):
                    msg3 += f"{i[1]} x {i[0].name}, "
                else:
                    msg3 += f"{i[1]} x {i[2]} {i[0].name}, "
            
            msg4 += f"{main.price:.2f}"
            price = currOrder.calc_price()
            msg5 += f"{price:.2f}"
            return render_template("custom_main_create.html", ing = system.ingredients, msg1 = msg1, msg2 = msg2, msg3 = msg3, msg4 = msg4, msg5 = msg5, msg6 = msg6)

        elif 'base_main' in request.form:
            if kind == 'burger':
                try:
                    main.checkBurger()
                except UserError as e:
                    msg2 = str(e)
                    for i in main.ingredients:
                        if isQIngredient(i[0]):
                            msg3 += f"{i[1]} x {i[0].name}, "
                        else:
                            msg3 += f"{i[1]} x {i[2]} {i[0].name}, "
                    msg4 += f"{main.price:.2f}"
                    price = currOrder.calc_price()
                    msg5 += f"{price:.2f}"
                    return render_template("custom_main_create.html", ing = system.ingredients, msg1 = msg1, msg2 = msg2, msg3 = msg3, msg4 = msg4, msg5 = msg5, msg6 = msg6)
                else:
                    return redirect(url_for('base_main'))
            else:
                return redirect(url_for('base_main'))

        elif 'side_drink' in request.form:
            if kind == 'burger':
                try:
                    main.checkBurger()
                except UserError as e:
                    msg2 = str(e)
                    for i in main.ingredients:
                        if isQIngredient(i[0]):
                            msg3 += f"{i[1]} x {i[0].name}, "
                        else:
                            msg3 += f"{i[1]} x {i[2]} {i[0].name}, "
                    msg4 += f"{main.price:.2f}"
                    price = currOrder.calc_price()
                    msg5 += f"{price:.2f}"
                    return render_template("custom_main_create.html", ing = system.ingredients, msg1 = msg1, msg2 = msg2, msg3 = msg3, msg4 = msg4, msg5 = msg5, msg6 = msg6)
                else:
                    return redirect(url_for('side_drink'))
            else:
                return redirect(url_for('side_drink'))

        elif 'checkout' in request.form:
            if kind == 'burger':
                try:
                    main.checkBurger()
                except UserError as e:
                    msg2 = str(e)
                    for i in main.ingredients:
                        if isQIngredient(i[0]):
                            msg3 += f"{i[1]} x {i[0].name}, "
                        else:
                            msg3 += f"{i[1]} x {i[2]} {i[0].name}, "
                    msg4 += f"{main.price:.2f}"
                    price = currOrder.calc_price()
                    msg5 += f"{price:.2f}"
                    return render_template("custom_main_create.html", ing = system.ingredients, msg1 = msg1, msg2 = msg2, msg3 = msg3, msg4 = msg4, msg5 = msg5, msg6 = msg6)
                else:
                    return redirect(url_for('checkout'))
            else:
                return redirect(url_for('checkout'))
        
    return render_template("custom_main_create.html", kind = request.args.get('kind'), ing = system.ingredients)

@app.route('/side_drink', methods=["GET", "POST"])
def side_drink():
    msg1 = ''
    msg2 = ''
    msg3 = 'Your sides and drinks so far: '
    msg4 = 'Your current order total is $'
    msg5 = ''
    currOrder = system.currOrder
    ingredients = system.ingredients
    errors = []
    addsuccesses = []
    delsuccesses = []

    if request.method == 'POST':
        if 'add' in request.form:
            for i in ingredients:
                if i.kind == 's' or i.kind == 'd':
                    if isQIngredient(i):
                        n = request.form.get(i.name)
                        if n != '':
                            n = int(n)
                            if n > 0:
                                try:
                                    currOrder.add_sideDrink(i, n, None)
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, ''])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    currOrder.del_sideDrink(i, n, None)
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, ''])

                    else: # isWIngredient
                        n = request.form.get('s' + i.name)
                        if n != '':
                            n.lstrip('0')
                            n = int(n)
                            if n > 0:
                                try:
                                    currOrder.add_sideDrink(i, n, 's')
                                except StockError as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, 's'])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    currOrder.del_sideDrink(i, n, 's')
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, 's'])

                        n = request.form.get('m' + i.name)
                        if n != '':
                            n = int(n)
                            if n > 0:
                                try:
                                    currOrder.add_sideDrink(i, n, 'm')
                                except StockError as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, 'm'])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    currOrder.del_sideDrink(i, n, 'm')
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, 'm'])

                        n = request.form.get('l' + i.name)
                        if n != '':
                            n = int(n)
                            if n > 0:
                                try:
                                    currOrder.add_sideDrink(i, n, 'l')
                                except StockError as e:
                                    errors.append(e)
                                else:
                                    addsuccesses.append([i.name, n, 'l'])
                            elif n < 0:
                                try:
                                    n = abs(n)
                                    currOrder.del_sideDrink(i, n, 'l')
                                except (UserError, StockError) as e:
                                    errors.append(e)
                                else:
                                    delsuccesses.append([i.name, n, 'l'])

            if addsuccesses:
                msg1 = 'Successfully added '
                for s in addsuccesses:
                    msg1 += str(s[1]) + ' ' + s[2]  + ' ' + s[0] + ', '
                msg1 += ' to your order.'
            
            if delsuccesses:
                msg5 = 'Successfully removed '
                for s in delsuccesses:
                    msg5 += str(s[1]) + ' ' + s[2]  + ' ' + s[0] + ', '
                msg5 += ' from your order.'

            if errors:
                for e in errors:
                    msg2 += str(e)
                    msg2 += ' '

            for i in currOrder.sideDrinks:
                if isQIngredient(i[0]):
                    msg3 += f"{i[1]} x {i[0].name}, "
                else:
                    msg3 += f"{i[1]} x {i[2]} {i[0].name}, "
            
            price = currOrder.calc_price()
            msg4 += f"{price:.2f}"
            return render_template("side_drink.html", ing = system.ingredients, msg1 = msg1, msg2 = msg2, msg3 = msg3, msg4 = msg4, msg5 = msg5)
        
    return render_template("side_drink.html", ing = system.ingredients)

@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    currOrder = system.currOrder
    mains = currOrder.mains
    sideDrinks = currOrder.sideDrinks

    if request.method == 'POST':
        if 'pay' in request.form:
            currOrder.change_status('cooking')
            return redirect(url_for('paid'))

    f = open("system.pickle", "wb")
    pickle.dump(system, f)

    return render_template("checkout.html", currOrder = currOrder, mains = mains, sideDrinks = sideDrinks)

@app.route('/paid')
def paid():
    currOrder = system.currOrder
    
    return render_template("paid.html", currOrder = currOrder)

@app.route('/view_order',methods=["GET","POST"])
def view_order():
    schOrder=[]

    if request.args.get('search_order') is not None:

        try:
            userinput=int(request.args.get('search_order'))
            schOrder.append(system.searchOrder(userinput))
        except ValueError:
            return render_template("Staff_viewOrder.html",results=system.orders,msg2="Order must be in numbers")
        except UserError:
            return render_template("Staff_viewOrder.html",results=system.orders,msg1="Order doesn't exit in system")
        else:
            return render_template("Staff_viewOrder.html",results=system.orders,order=schOrder)
            

    return render_template("Staff_viewOrder.html",results=system.orders)

@app.route('/notify_customer',methods=["GET","POST"])
def notify_customer():
    if request.method=="POST":
        ordersid=int(request.form.get('notify'))
        system.deleteOrder(ordersid)
        return render_template("notifycation.html")


@app.route('/updated_status',methods=["GET","POST"])
def updated_status():

 
    if request.method=="POST":
        if 'ready' in request.form:

            system.updateOrderStatus(int(request.form.get('ready')),'ready for pickup')
        else:
            system.updateOrderStatus(int(request.form.get('cooking')),'cooking')

    f = open("system.pickle", "wb")
    pickle.dump(system, f)
                
    return render_template("Staff_viewOrder.html", results=system.orders)


