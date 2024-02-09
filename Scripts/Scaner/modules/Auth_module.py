# Проверка пароля пользователя
from Server.app.ms.profiler import *

def get_text(host,pas,login,port,who_req):
    p = profiler(find_path(f"{who_req}", ndir=1))

    report=""
    if len(pas)==0:
        report+="ПАРОЛЬ НЕ УСТАНОВЛЕН!! УСТАНОВИТЕ ПАРОЛЬ"
        p.plus_value(key="red",amount=1)
        return report
    weak_passwords=["root","123",f"{login}","admin"]
    if len(pas)<=9:
        report+="Пароль сервера меньше 9 символов, сделайте его больше"
        p.plus_value(key="yellow",amount=1)
        report+="\n"
    if pas in weak_passwords:
        report+="Пароль слишком простой измените его для большей безопастности"
        report += "\n"

        if pas==weak_passwords[2]:
            report+="!!ПАРОЛЬ СОДЕРЖИТ ИМЯ ПОЛЬЗОВАТЕЛЯ ИЗМЕНИТЕ ПАРОЛЬ!!"
            report += "\n"
            p.plus_value("red",amount=1)
    return report