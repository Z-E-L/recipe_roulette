from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    cuisine = StringField('Cuisine')
    dietary_info = StringField('Dietary Information')
    submit = SubmitField('Add Recipe')


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')