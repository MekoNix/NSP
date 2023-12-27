from flask import *
from Server.app.ms.login import *


app = Flask(__name__)
app.secret_key = "asdasd"
@app.route('/')
def hello_world():
    return 'Привет, мир!'

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
            return redirect("/2")
        else:
            return "Login or password is incorrect"

    return render_template('login.html')
@app.route("/2")
@login_required
def dwa():
    return "it not work "


if __name__ == '__main__':
    app.run(debug=True)
