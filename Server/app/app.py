from flask import *
from Server.app.ms.login import *
from Server.app.ms.WSGI import *
from Server.app.ms.singup import *

app = Flask(__name__)
app.secret_key = "asdasd"
@app.route('/')
def hello_world():

    return 'Привет, мир!'
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
            return redirect("/2")
        else:
            return "Login or password is incorrect"

    return render_template('login.html')
@app.route("/register", methods=['GET', 'POST'])
def register():
    error=None
    try:
        if request.method=="POST":
            username = request.form['username']
            password = request.form['password']
            sing_up(username, password)
            return redirect(url_for("2"))
    except Exception as e:
        log_event(f"Error occurred while creating user {e} ")
        error=f"Error occurred while creating user {e} "
    return render_template('signup.html',error=error)

# BLOCK AUTH END
@app.route("/2")
@login_required
def dwa():
    return "it not work "


if __name__ == '__main__':
    app.run(debug=True)
