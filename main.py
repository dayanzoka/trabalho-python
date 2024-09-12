from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from config import app
from forms import EventForm
from models import *


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegisterForm
    from werkzeug.security import generate_password_hash

    formulario = RegisterForm()

    if formulario.validate_on_submit():
        usu = formulario.username.data
        sen = generate_password_hash (formulario.password.data)
        print(f'-- {usu} -- {sen}')

        usu_ex = User.query.filter_by(username=usu).first()

        if usu_ex:
            print('Usuario já existe')
        else:
            novo_usuario = User(username=usu, password=sen)
            db.session.add(novo_usuario)
            db.session.commit()
            print('Usuário criado')
            #redirecionar
            return  redirect(url_for('login'))


    return render_template('register.html', form=formulario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    from werkzeug.security import check_password_hash

    formulario = LoginForm()

    if formulario.validate_on_submit():
        usuStr = formulario.username.data

        usuBanco = User.query.filter_by(username=usuStr).first()

        if usuBanco:
            senhaDigitada = formulario.password.data
            senhaBanco = usuBanco.password

            if check_password_hash(senhaBanco, senhaDigitada):
                login_user(usuBanco)
                return redirect(url_for('dashboard'))
            #else:

    return render_template('login.html', form=formulario)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    meus_eventos = Event.query.filter(Event.user_id == current_user.id).all()
    todos_eventos = Event.query.all()

    return render_template('dashboard.html', meus_eventos=meus_eventos, todos_eventos=todos_eventos)



@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    formulario = EventForm()

    if formulario.validate_on_submit():
        novo_evento = Event(
            event_name=formulario.event_name.data,
            event_date=formulario.event_date.data,
            description=formulario.description.data,
            status=formulario.status.data,
            user_id=current_user.id,
        )
        db.session.add(novo_evento)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('create_event.html', form=formulario)



@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    evento = Event.query.get_or_404(event_id)

    if evento.owner != current_user and evento.assigned_user != current_user:
        return redirect(url_for('dashboard'))

    formulario = EventForm(obj=evento)

    if formulario.validate_on_submit():
        evento.event_name = formulario.event_name.data
        evento.event_date = formulario.event_date.data
        evento.description = formulario.description.data
        evento.status = formulario.status.data
        evento.assigned_to = formulario.assigned_to.data.id if formulario.assigned_to.data else None
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit_event.html', form=formulario)


@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()

    if event:
        db.session.delete(event)
        db.session.commit()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)