import requests
from flask import *
from flask_login import *
from Server.app.ms.login import *
from Server.app.ms.WSGI import *
from Server.app.ms.singup import *
import os
from Scripts.Scaner.scanner import Scanner
import subprocess


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
    user_directory = find_path(f"{username}", ndir=1)
    try:
        files_info = []
        html_files = [file for file in os.listdir(user_directory) if file.endswith('.html')]
        for html_file in html_files:
            birthday = get_birthday_file(html_file, username)
            files_info.append({"name": html_file, "birthday": birthday})
        return jsonify(files_info)
    except FileNotFoundError:
        return jsonify({"error": "User directory not found"}), 404

@login_required
@NSP.route('/users/<username>/<filename>')
def serve_html_file(username,filename):
    user_directory = find_path(f"{username}",ndir=1)
    return send_from_directory(user_directory, filename)


@login_required
@NSP.route('/api/download-pdf/<username>/<filename>')
def download_pdf(username, filename):
    html_file_path = find_path(f"{username}", ndir=1) + f'/{filename}'
    pdf_file_path = html_file_path.replace('.html', '.pdf')
    filename=filename.replace(".html",'.pdf')
    # Определяем URL, который нужно преобразовать в PDF

    # Вызываем скрипт pdf_generator.py с помощью subprocess
    subprocess.run(["python", find_path("html_to_pdf.py"), html_file_path, pdf_file_path])
    # Отправляем файл
    return send_from_directory(find_path(f"{username}",ndir=1),filename)

    # Отправляем файл
    return send_from_directory(pdf_file_path, filename)


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