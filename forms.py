from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms import SelectField
from wtforms_sqlalchemy.fields import QuerySelectField

from models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EventForm(FlaskForm):
    event_name = StringField('Nome do Evento', validators=[DataRequired()])
    event_date = DateField('Data do Evento', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])


    status = SelectField('Status', choices=[('Pendente', 'Pendente'), ('Em andamento', 'Em andamento'),
    ('Concluída', 'Concluída')], default='Pendente')

    # Campo para atribuir o evento a outro usuário
    assigned_to = QuerySelectField('Atribuir a', query_factory=lambda: User.query.all(), allow_blank=True,
    get_label='username')

    submit = SubmitField('Criar Evento')
