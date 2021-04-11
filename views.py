from flask import render_template, session, redirect, request
from datetime import datetime

from init import db, app
from forms import LoginForm, RegistrationForm, OrderForm
from tables import User, Dish, Category, Order
from words import correct_word


@app.route("/")
def render_main():
    items = db.session.query(Dish)
    categories = db.session.query(Category)
    session["word"] = correct_word(len(session.get("cart", [])))
    user = None
    if session.get("user_id"):
        user = User.query.filter(User.id == session.get("user_id")).first()
    return render_template("main.html", categories=categories, items=items, dishes=session.get("cart", []), user=user)


@app.route("/cart/", methods=["GET", "POST"])
def render_cart():
    flag = 0
    form = OrderForm()
    cart = session.get("cart", [])
    use_it = set()
    new_cart = []
    for item in cart:
        if item not in use_it:
            new_cart.append(item)
            use_it.add(item)
    user = None
    if session.get("user_id"):
        user = User.query.filter(User.id == session.get("user_id")).first()
    session["word"] = correct_word(len(session.get("cart", [])))
    return render_template("cart.html", form=form, new_cart=new_cart, flag=flag, user=user)


@app.route("/add/<item>/")
def add_to_cart(item):
    flag = 0
    form = OrderForm()
    items = db.session.query(Dish)
    cart = session.get("cart", [])
    cart.append(item)
    session["cart"] = cart
    for i in items:
        if i.title == item:
            if not session.get("price"):
                session["price"] = 0
            session["price"] += i.price
    cart = session.get("cart", [])
    use_it = set()
    new_cart = []
    for item in cart:
        if item not in use_it:
            new_cart.append(item)
            use_it.add(item)
    user = None
    if session.get("user_id"):
        user = User.query.filter(User.id == session.get("user_id")).first()
    session["word"] = correct_word(len(session.get("cart", [])))
    return render_template("cart.html", form=form, flag=flag, new_cart=new_cart, user=user)


@app.route("/pop/<item>/")
def pop_from_cart(item):
    flag = 1
    form = OrderForm()
    items = db.session.query(Dish)
    cart = session.get("cart", [])
    cart.remove(item)
    session["cart"] = cart
    for i in items:
        if i.title == item:
            session["price"] -= i.price
    cart = session.get("cart", [])
    use_it = set()
    new_cart = []
    for item in cart:
        if item not in use_it:
            new_cart.append(item)
            use_it.add(item)
    user = None
    if session.get("user_id"):
        user = User.query.filter(User.id == session.get("user_id")).first()
    session["word"] = correct_word(len(session.get("cart", [])))
    return render_template("cart.html", form=form, flag=flag, new_cart=new_cart, user=user)


@app.route("/ordered/", methods=["GET", "POST"])
def render_order():
    form = OrderForm()
    if request.method == "POST":
        id_o = len(db.session.query(User).get(session["user_id"])) + 1
        date = datetime.now().date()
        mail = form.mail.data
        name = form.name.data
        address = form.address.data
        user_id = session["user_id"]
        sum_price = session["price"]
        dishes = session.get("cart", [])
        order = Order(id=id_o, date=date, mail=mail, name=name, address=address, user_id=user_id, sum_price=sum_price,
                      dishes=dishes)
        db.session.add(order)
        db.session.commit()
        return render_template("ordered.html")
    else:
        orders = db.session.query(Order)
        return render_template("cart.html", orders=orders)


@app.route("/account/", methods=["GET", "POST"])
def render_account():
    return render_template("account.html")


@app.route("/login/", methods=["GET", "POST"])
def render_login():
    if session.get("user_id"):
        return redirect("/")
    form = LoginForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("login.html", form=form)
        user = User.query.filter(User.mail == form.mail.data).first()
        if not user or user.password_valid(form.password.data) != form.password.data:
            form.mail.errors.append("Неверно указана почта или пароль")
        else:
            session["user_id"] = user.id
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout/", methods=["GET"])
def logout():
    if session.get("is_auth"):
        session.pop("is_auth")
    if session.get("user_id"):
        session.pop("user_id")
    return redirect("/")


@app.route("/registration/", methods=["GET", "POST"])
def registration():
    if session.get("user_id"):
        return redirect("/")
    form = RegistrationForm()
    if request.method == "POST":
        user = User()
        user.mail = form.mail.data
        user.password_hash = form.password.data
        user_ = User.query.filter_by(mail=user.mail).first()
        if user_:
            form.mail.errors.append("Пользователь под такой почтой уже зарегистрирован")
        db.session.add(user)
        db.session.commit()
        return render_template("registration_success.html", form=form, mail=user.mail)
    return render_template("registration.html", form=form)


@app.errorhandler(404)
def render_not_found(error):
    return render_template("error.html", error=error), 404


@app.errorhandler(500)
def render_server_error(error):
    return render_template("error.html", error=error), 500
