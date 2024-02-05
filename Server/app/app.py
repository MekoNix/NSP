import requests
from flask import *
from flask_login import *
from Server.app.ms.login import *
from Server.app.ms.WSGI import *
from Server.app.ms.singup import *
from datetime import datetime
import os
from Server.cli.report import create_pdf_report


NSP = Flask(__name__)
NSP.secret_key = "J!#ascva#GFA2444!#SA"
@NSP.route('/')
def hello_world():

    return redirect(url_for('login'))
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
@NSP.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    user = current_user.username
    path = find_path(nroot=1) + f"/Server/Users/profiles/{user}"
    file_path = os.path.join(path, file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully'}), 200

@NSP.route('/api/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    user = current_user.username
    path = find_path(nroot=1) + f"/Server/Users/profiles/{user}"
    if not os.path.exists(os.path.join(path, filename)):
        abort(404)
    return send_from_directory(path, filename, as_attachment=True)

#API BLOCK END
@NSP.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    user = str(current_user.username)

    if request.method == 'POST':
        data = request.json  # data[whattoneed]
        #ТЕСТОВАЯ key УБРАТЬ НА РЕЛИЗЕ
        key_value_pairs = {
            "Host Port": data["host"]+":"+data["port"],

        }
        wsgi_test(data["host"],user)
        return jsonify({"status": "success", "message": "Данные получены"})

    return render_template("dashboard.html", username=user)

if __name__ == '__main__':
    NSP.run()