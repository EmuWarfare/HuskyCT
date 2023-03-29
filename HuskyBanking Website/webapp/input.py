from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.form import Form

#General Guide
#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

#CSRF and Fields link
#https://wtforms.readthedocs.io/en/3.0.x/csrf/
#https://wtforms.readthedocs.io/en/3.0.x/fields/

#class used to store input objects used in the main page

class baseForm(FlaskForm):
    class Meta:
        csrf = False    #turns CSRF off, put true to turn it back on, also need to use validators in routes.py for it to work, and enable the hidden tag in html


class LoginInput(baseForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    customPage = SubmitField("Custom Page")
    submit = SubmitField('Sign In')

class UserPageLogout(baseForm):
    logOut = SubmitField('Logout')


class TransferInput(baseForm):
    username = StringField('Username')
    moneyAmount = StringField('Money Amount')
    transfer = SubmitField('Transfer Money')