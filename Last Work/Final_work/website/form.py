# Import the required modules from flask and wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import IntegerField, SelectField


# Create a ScheduleCollectionForm class that inherits from FlaskForm
class ScheduleCollectionForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    collection_date = DateField('Collection Date', validators=[DataRequired()])
    collection_time = TimeField('Collection Time', validators=[DataRequired()])
    submit = SubmitField('Schedule Collection')

# Create a TrackRecyclingForm class that inherits from FlaskForm
class TrackRecyclingForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    materials = TextAreaField('Recycled Materials', validators=[DataRequired()])
    status = SelectField('Status', choices=[('collected', 'Collected'), ('not_collected', 'Not Collected')], validators=[DataRequired()])
    submit = SubmitField('Track Recycling')