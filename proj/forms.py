from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError, Regexp
from proj.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
'Usernames must have only letters, ' 'numbers, dots or underscores')]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit =SubmitField('Sign Up')   
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower().strip()).first()      
        if user:
            raise ValidationError(f'{username.data} is already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower().strip()).first()        
        if user:
            raise ValidationError(f'{email.data} is already taken!')
            
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
'Usernames must have only letters, ' 'numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')
      
    def validate_username(self, username):
        if username.data.lower().strip() != current_user.username:
            user = User.query.filter_by(username=username.data.lower().strip()).first()      
            if user:
                raise ValidationError(f'{username.data} is already taken!')

    def validate_email(self, email):
        if email.data.lower().strip() != current_user.email:
            user = User.query.filter_by(email=email.data.lower().strip()).first()        
            if user:
                raise ValidationError(f'{email.data} is already taken!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')
    
class UserForm(FlaskForm):
    userid = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Input User Id"})
    submit = SubmitField('View Info')
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    username = StringField('', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
'Usernames must have only letters, ' 'numbers, dots or underscores')], render_kw={"placeholder": "Search username"})
    submit = SubmitField('search')
    
    

    