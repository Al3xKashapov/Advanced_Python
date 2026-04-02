"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from hw1_3.hw2_validators import number_length, NumberLength
from wtforms.validators import InputRequired, Email, Length, NumberRange

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField(validators=[
        InputRequired(message="Email is required"),
        Email(message="Invalid email format")
    ])
    phone = IntegerField(validators=[
        InputRequired(message="Phone is required"),
        NumberRange(min=0, message="Phone must be positive"),
        number_length(min=10, max=10, message="Phone must be exactly 10 digits"),
        NumberLength(min=10, max=10, message="Phone must be exactly 10 digits")
    ])
    name = StringField(validators=[
        InputRequired(message="Name is required")
    ])
    address = StringField(validators=[
        InputRequired(message="Address is required")
    ])
    index = IntegerField(validators=[
        InputRequired(message="Index is required"),
        NumberRange(min=0, message="Index must be positive")
    ])
    comment = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data
        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
