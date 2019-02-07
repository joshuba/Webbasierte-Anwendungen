import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from sqlalchemy.exc import SQLAlchemyError
from config import config
from flask import session
from models import *

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
app.app_context().push()  # TODO bekomme nur so Datenbankzugriff im Code


@app.route('/', methods=['GET', 'POST'])
def index():
    session["perpage"] = 20  # legt perPage zu beginn fest
    if 'cart' not in session or session.get("cart") == None:
        session['cart'] = []  # erstelle Leeren Warenkorb

    # wenn keine usersession mit dem aktuell eingeloggtem user existiert
    if session.get("actUser") is None:
        return redirect("/login")
    else:  # ein User ist eingeloggt
        flash('Erfolgreich angemeldet')

        return redirect("/users")


@app.route('/users', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/users/page/<int:page>')
def showUsers(page):
    if not checkAuth():
        return redirect("/login")

    # wenn auf ein perpage geklickt wurde, merke in session
    if request.args.get("perpage"):
        session["perpage"] = request.args.get("perpage")

    page, lastpage = correctPage(page, Customer.query.count())  # falls zu oft nach links oder rechts geklickt wird
    users = Customer.query.order_by(Customer.customerid).paginate(per_page=int(session["perpage"]), page=page,
                                                                  error_out=True)

    return render_template('users.html', username=session.get("actUser"), users=users, page=users.page,
                           lastpage=lastpage, cartlength=len(session['cart']))


@app.route('/orders', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/orders/page/<int:page>')
def showOrders(page):
    if not checkAuth():
        return redirect("/login")

    # wenn auf ein perpage geklickt wurde, merke in session
    if request.args.get("perpage"):
        session["perpage"] = request.args.get("perpage")

    page, lastpage = correctPage(page, Order.query.count())  # falls zu oft nach links oder rechts geklickt wird
    orders = Order.query.paginate(per_page=int(session["perpage"]), page=page, error_out=True)

    return render_template('orders.html', username=session.get("actUser"), orders=orders, page=orders.page,
                           lastpage=lastpage)


@app.route('/products', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/products/page/<int:page>')
def showProducts(page):
    if not checkAuth():
        return redirect("/login")

    # wenn auf ein perpage geklickt wurde, merke in session
    if request.args.get("perpage"):
        session["perpage"] = request.args.get("perpage")

    page, lastpage = correctPage(page, Product.query.count())  # falls zu oft nach links oder rechts geklickt wird
    products = Product.query.paginate(per_page=int(session["perpage"]), page=page, error_out=True)

    return render_template('products.html', username=session.get("actUser"), products=products, page=products.page,
                           lastpage=lastpage, cartlength=len(session['cart']))


@app.route('/users/<id>', methods=['Get'])
def userDetail(id):
    customer = Customer.query.filter_by(customerid=id).first()
    orders = Order.query.filter_by(customerid=id).join(t_orderlines).join(Product).all()  # alle Bestellungen

    return render_template('user.html', customer=customer, username=session.get("actUser"), orders=orders)


@app.route('/users/<id>/orderdetail', methods=['get'])
def orderDetail(id):
    orders = Order.query.filter_by(customerid=id).join(t_orderlines).join(Product).all()  # alle Bestellungen

    return render_template('oder.html', username=session.get("actUser"), orders=orders)


def checkInventory(id):
    """Checkt ob ein Produkt hinzugefügt werden kann"""
    alreadyInCart = 0
    s = session["cart"]
    # Berechne wie oft das Produkt schon im Einkaufswagen ist
    for ele in s:
        if ele == id:
            alreadyInCart += 1

    inventory = Inventory.query.filter_by(prod_id=id).first()
    if inventory.quan_in_stock > alreadyInCart:
        return True
    else:
        return False


@app.route('/addtocart/<prodID>', methods=['POST'])
def addtocart(prodID):
    if checkInventory(prodID):
        cart_list = session['cart']
        cart_list.append(prodID)
        session['cart'] = cart_list
        flash('Erfolgreich hinzugefügt', "error")
    else:
        flash('Kein weiterer Bestand mehr auf Lager')
    return redirect("/products/page/1")


@app.route('/cart/delete/<int:id>', methods=['GET'])
def deleteFromCart(id):
    id -= 1
    s = session['cart']
    del s[id]
    session['cart'] = s

    return redirect("/cart")


@app.route('/cart')
def showCart():
    l = []
    cartlist = session['cart']
    for prodId in cartlist:
        product = Product.query.filter_by(prod_id=prodId).first()
        l.append(product)

    return render_template("cart.html", cart=l)


@app.route('/cart/order', methods=['POST'])
def addOrder():
    items = {}
    for ele in session["cart"]:
        if ele not in items.keys():
            items[ele] = 1
        else:
            items[ele] = items.get(ele) + 1

    cust = Customer.query.filter_by(username=session["actUser"]).one()
    total = getTotalFromCart()
    date = str(datetime.now())
    newOrder = Order(
        orderdate=date,
        customer=cust,
        netamount=total / 1.07,
        tax=total * 0.07,
        totalamount=total
    )
    db.session.flush()
    try:
        db.session.add(newOrder)
        db.session.commit()
        session["cart"] = []

        return redirect(url_for('userDetail', id=cust.customerid))
    except SQLAlchemyError as err:
        return None


@app.route('/users/edit/<id>', methods=['POST'])
def editUser(id):
    customer = Customer.query.filter_by(customerid=id).first()
    if request.form:
        customer = Customer.query.filter_by(customerid=id).first()
        customer.firstname = request.form.get("vorname")
        customer.lastname = request.form.get("nachname")
        customer.address1 = request.form.get("adresse")
        customer.city = request.form.get("stadt")
        customer.state = request.form.get("staat")
        customer.zip = request.form.get("plz")
        customer.country = request.form.get("land")
        customer.email = request.form.get("email")
        customer.phone = request.form.get("phone")
        customer.username = request.form.get("username")
        customer.age = request.form.get("alter")
        customer.gender = request.form.get("geschlecht")
        customer.password = request.form.get("password")

        db.session.commit()
        return redirect("users/" + id)

    return render_template("userEdit.html", username=session.get("actUser"), customer=customer)


@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    id = request.args.get("removeID")
    customer = Customer.query.filter_by(customerid=id).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    inputUser = request.form.get("username")
    inputPW = request.form.get("password")

    # Wenn noch kein User eingeloggt ist oder Daten eingegeben hat:
    if inputUser or inputPW:
        if auth_user(inputUser, inputPW):
            session["actUser"] = inputUser  # setze session
            return redirect("/")
        else:
            return render_template('logIn.html', meldung="!!! Entweder Username oder Passwort Falsch eingegeben !!!")
    else:
        return render_template('logIn.html')


@app.route('/users/search')
def user_search():
    if not checkAuth():
        return redirect("/login")

    return render_template("user_search.html")


@app.route('/users/search/<int:page>', methods=['GET', 'POST'])
def search(page):
    if not checkAuth():
        return redirect("/login")

    if request.args.get("search"):
        begriff = request.args.get("search")

    sortBy = "userID"
    if request.args.get("sortBy"):
        sortBy = request.args.get("sortBy")

    # wenn auf ein perpage geklickt wurde, merke in session
    if request.args.get("perpage"):
        session["perpage"] = request.args.get("perpage")

    users = Customer.query.filter(
        Customer.username.contains(begriff) |
        Customer.email.contains(begriff) |
        Customer.firstname.contains(begriff) |
        Customer.lastname.contains(begriff))

    page, lastpage = correctPage(page, users.count())  # falls zu oft nach links oder rechts geklickt wird
    users = users.paginate(per_page=int(session["perpage"]), page=page, error_out=True).items

    return render_template("search_results.html", username=session.get("actUser"), results=users, page=page,
                           lastpage=lastpage, begriff=begriff)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


def checkAuth():
    # wenn keine usersession mit dem aktuell eingeloggtem user existiert
    if session.get("actUser") is None:  # TODO richtiges Sessionmanagement implementieren
        return False
    else:
        return True


def correctPage(page, anz):
    """Korrigiert die Seitenzahl, je nachdem wie viele Einträge auf einer Seite sind"""
    perpage = int(session.get("perpage"))
    if perpage > anz:
        return page, anz
    if page < 1:
        page = 1
    if page >= anz / perpage:  # setze seite auf das maximum, wenn man von kleiner perpage auf große wechselt (Auf letzer seite)
        page = int(anz / perpage)

    return page, anz / perpage


def auth_user(name, password):
    """Gleicht Username und Passwort mit der Datenbank ab"""
    user = Customer.query.filter_by(username=name).first()
    if user and user.password == password:
        return True
    else:
        return False


def getTotalFromCart():
    total = 0.0
    for id in session["cart"]:
        total += float(Product.query.filter_by(prod_id=id).first().price)
    return total


if __name__ == "__main__":
    app.run(debug=True)
