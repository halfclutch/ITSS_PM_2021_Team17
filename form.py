from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import IntegerField, StringField, SelectField, FileField, validators
from wtforms.validators import DataRequired

class CyclistInfo(FlaskForm):
    Weight = IntegerField(u'Weight (kg)', validators=[DataRequired()])
    Speed = IntegerField(u'Speed (km/hr)', validators=[DataRequired()])
    Apparel = SelectField(u'Apparel', choices=[('Skinsuit', 'Skinsuit'),('Jersey', 'Jersey')])
    Helmet = SelectField(u'Helmet', choices=[('Aero-helmet', 'Aero-helmet'),('Road-helmet', 'Road-helmet')])
    Frame = SelectField(u'Frame', choices=[('Tri-bike', 'Tri-bike'),('Road-bike', 'Road-bike')])
    Wheels = SelectField(u'Wheels', choices=[('Aero-wheels', 'Aero-wheels'),('Normal Box Rim', 'Normal Box Rim')])
    Bars = SelectField(u'Bars', choices=[('Aero-bars', 'Aero-bars'),('Normal Drop Bars', 'Normal Drop Bars')])
    Staying_in_Position = SelectField(u'Staying in Position', choices=[('Yes', 'Yes'),('No', 'No') ])
    Image = FileField(u'Image', validators=[FileRequired()])



