from flask import *
from Server.app.ms.login import *
from Server.app.ms.WSGI import *
from Server.app.ms.singup import *

app = Flask(__name__)
app.secret_key = "asdasd"
@app.route('/')
def hello_world():

    return "123"
# BLOCK AUTH START
@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.pop('authenticated', None)

    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_web(username, password) == 1:
            session['authenticated'] = True
            return redirect(url_for('dwa'))
        else:
            return "Incorrect username or password", 401

    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
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
@app.route("/2")
@login_required
def dwa():
    return "It work "


if __name__ == '__main__':
    app.run(debug=True)
