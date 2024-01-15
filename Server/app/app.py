import requests
from flask import *
from flask_login import *
from Server.app.ms.login import *
from Server.app.ms.WSGI import *
from Server.app.ms.singup import *

NSP = Flask(__name__)
NSP.secret_key = "J!#ascva#GFA2444!#SA"
@NSP.route('/')
def hello_world():

    return "123"
# BLOCK AUTH START
login_manager=LoginManager()
login_manager.init_app(NSP)
@login_manager.user_loader
def load_user(username):
    return User(username)
@NSP.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    logout_user()
    session.clear()
    # Перенаправление на  страницу входа
    return redirect(url_for('login'))

@NSP.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        acs=login_web(username,password)
        if acs:
            login_user(acs)
            return redirect("/dashboard")
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
#API BLOCK START
@NSP.route("/api/get-files")
def get_files():
    user=current_user.username
    path=find_path(nroot=1)+f"/Server/Users/profiles/{user}"
    files=[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return jsonify(files)
    # Требует дорабтик НУжно что бы можно ьыло скачивать файлы.
#API BLOCK STOP
@NSP.route("/dashboard")
@login_required
def dashboard():
    user=str(current_user.username)
    return render_template("dashboard.html",username=user)

if __name__ == '__main__':
    NSP.run()