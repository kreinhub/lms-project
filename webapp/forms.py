from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp

regexp = r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z\S+]{8,}'


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()],
                           render_kw={"class": "form-control", "placeholder": "Enter email", "type": "email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"class": "form-control", "placeholder": "Enter Password", "type": "password"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary", "Type": "submit"})


class RegistrationForm(FlaskForm):

    email = StringField('Email',
                               render_kw={"class": "form-control", "placeholder": "Enter email", "type": "email"})
    password_reg = PasswordField('Password', validators=[DataRequired(), Regexp(regexp)],
                                 render_kw={"class": "form-control", "placeholder": "Enter Password",
                                            "type": "password"})
    password_reg_confirm = PasswordField('Password', validators=[DataRequired(), Regexp(regexp)],
                                 render_kw={"class": "form-control", "placeholder": "Confirm Password",
                                            "type": "password"})
    submit_reg = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary", "Type": "submit"})