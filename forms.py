from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    mail = StringField("Электронная почта:", validators=[DataRequired()])

    password = PasswordField("Пароль:", validators=[
        DataRequired(),
        Length(min=8, message="Пароль должен быть не менее 8 символов"),
        EqualTo('confirm_password', message="Пароли не одинаковые")
    ])


class RegistrationForm(FlaskForm):
    mail = StringField("Электронная почта")
    password = PasswordField("Пароль")


class OrderForm(FlaskForm):
    date = StringField("Дата")
    mail = StringField("Электронная почта")
    name = StringField("Имя")
    phone = StringField("Телефон")
    address = StringField("Адрес")
    submit = SubmitField("Оформить заказ")
