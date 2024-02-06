import requests
from flask import *
from flask_login import *
from Server.app.ms.login import *
from Server.app.ms.WSGI import *
from Server.app.ms.singup import *
from datetime import datetime
import os
from Server.cli.report import create_pdf_report
from Scripts.Scaner.scanner import Scanner

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

@login_required
@NSP.route('/api/data/<username>/pf')
def serve_json_file(username):
    return send_from_directory(find_path(f"{username}",ndir=1), 'pf.json')


@login_required
@NSP.route('/api/get-html-files/<username>')
def list_html_files(username):
    user_directory = find_path(f"{username}",ndir=1)
    try:
        html_files = [file for file in os.listdir(user_directory) if file.endswith('.html')]
        return jsonify(html_files)
    except FileNotFoundError:
        return jsonify({"error": "User directory not found"}), 404

@login_required
@NSP.route('/users/<username>/<filename>')
def serve_html_file(username,filename):
    user_directory = find_path(f"{username}",ndir=1)
    return send_from_directory(user_directory, filename)

#API BLOCK END
@NSP.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    user = str(current_user.username)
    if request.method == 'POST':
        data = request.json  # data[whattoneed]
        scanner = Scanner(login=data["login"], password=data["pass"], host=data["host"], port=data["port"], who_req=f"{user}", title=data["host"],comment=data["comment"])
        scanner.scan()
        return jsonify({"status": "success", "message": "Данные получены"})
    return render_template("dashboard.html", username=user)

if __name__ == '__main__':
    NSP.run(debug=True)