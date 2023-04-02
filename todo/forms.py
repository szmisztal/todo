from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    expense = StringField('Expense', validators = [DataRequired()])
    cost = FloatField('Cost', validators = [DataRequired()])
    paid = BooleanField('Paid', default = False)