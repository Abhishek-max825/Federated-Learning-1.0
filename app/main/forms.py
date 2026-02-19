from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired

class PredictionForm(FlaskForm):
    age_group = SelectField('Age Group', choices=[
        ('1.0', '18 to 24'), ('2.0', '25 to 29'), ('3.0', '30 to 34'), 
        ('4.0', '35 to 39'), ('5.0', '40 to 44'), ('6.0', '45+')
    ], validators=[DataRequired()])
    
    sex = SelectField('Sex', choices=[
        ('1.0', 'Male'), ('2.0', 'Female')
    ], validators=[DataRequired()])
    
    bmi = FloatField('BMI (e.g. 25.5)', validators=[DataRequired()])
    
    smoked_100_cigarettes = SelectField('Smoked at least 100 cigarettes?', choices=[
        ('1.0', 'Yes'), ('2.0', 'No'), ('Unknown', 'Unknown')
    ], validators=[DataRequired()])
    
    diabetes_diagnosis = SelectField('Diabetes Diagnosis', choices=[
        ('1.0', 'Yes'), ('2.0', 'Yes (Pregnancy)'), ('3.0', 'No'), 
        ('4.0', 'No, pre-diabetes'), ('Unknown', 'Unknown')
    ], validators=[DataRequired()])
    
    heart_attack_history = SelectField('History of Heart Attack', choices=[
        ('1.0', 'Yes'), ('2.0', 'No'), ('Unknown', 'Unknown')
    ], validators=[DataRequired()])
    
    stroke_history = SelectField('History of Stroke', choices=[
        ('1.0', 'Yes'), ('2.0', 'No'), ('Unknown', 'Unknown')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Predict')
