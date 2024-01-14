from flask import *
from Server.app.ms.login import *
from Server.app.ms.WSGI import *
from Server.app.ms.singup import *

NSP = Flask(__name__)
NSP.secret_key = "asdasd"
@NSP.route('/')
def hello_world():

    return "123"
# BLOCK AUTH START
@NSP.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.pop('authenticated', None)

    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('login'))

@NSP.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_web(username, password) == 1:
            session['authenticated'] = True
            return redirect(url_for('home'))
        else:
            return "Incorrect username or password", 401

    return render_template('login.html')

@NSP.route("/signup", methods=['GET', 'POST'])
def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if sign_up(username, password) == 1:
                return redirect(url_for('login'))
            else:
                return "A user with this username already exists", 401

        # Отображение страницы регистрации
        return render_template('signup.html')
# BLOCK AUTH END
@NSP.route("/home")
@login_required
def home():
    return "It work "


if __name__ == '__main__':
    WSGI(NSP=NSP)