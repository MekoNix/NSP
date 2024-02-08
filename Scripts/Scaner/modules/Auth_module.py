# Проверка пароля пользователя

def get_text(host,pas,login,port):
    report=""
    weak_passwords=["root","123",f"{login}","admin"]
    if len(pas)<=9:
        report+="Пароль сервера меньше 9 символов, сделайте его больше"
        report+="\n"
    if pas in weak_passwords:
        report+="Пароль слишком слабый измените его для большей безопастности"
        report += "\n"
        if pas==weak_passwords[2]:
            report+="!!ПАРОЛЬ СОДЕРЖИТ ИМЯ ПОЛЬЗОВАТЕЛЯ ИЗМЕНИТЕ ПАРОЛЬ!!"
            report += "\n"
    return report
