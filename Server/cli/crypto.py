import os
from cryptography.fernet import Fernet
import datetime
from Scripts.modules import *
from Scripts.log import log_event

import json
import hashlib


def create_db():
    if not find_path("Users",ndir=1):
        os.mkdir(find_path("Server",ndir=1)+"/Users")
        os.mkdir(find_path("Users", ndir=1)+"/db")
        os.mkdir(find_path("Users", ndir=1) + "/profiles")
    else:
        pass
# ВНИМАНИЕ CRYPTO PY отключён до лучших времён

# Путь к файлу с ключом
key_file = find_path(nroot=1)+"/Server/Users/db/key"

# Путь к файлу с данными





# Функция для загрузки ключа из файла
def load_key():
    create_db()
    if find_path("key"):
        with open(key_file, 'rb') as file:
            return file.read()
    else:
        # Функция для генерации и сохранения нового ключа
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
        return load_key()
# Функция для шифрования данных
file_path= find_path(nroot=1)+"/Server/Users/db/users.json"

def encrypt_data(file_path=file_path):
    key = load_key()

    fernet = Fernet(key)
    file_path = find_path("users.json")
    try:
        with open(file_path, 'r') as file:
            data = file.read()
        encrypted_data = fernet.encrypt(data.encode())
        path=file_path[:-11]+'/enc'
        with open(path, 'wb') as file:
            file.write(encrypted_data)
        os.remove(find_path('users.json'))
    except Exception as e:
        print(f"Произошла ошибка при шифровании данных: {e}")
        return e

# Функция для расшифровки данных
def decrypt_data(file_path=find_path(nroot=1)+'/Server/Users/db/enc'):
    key = load_key()
    # Создаем объект Fernet с предоставленным ключом
    fernet = Fernet(key)
    # Читаем зашифрованные данные из файла
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode()
    # Расшифровываем данные и возвращаем их
    # try:
    #     decrypted_data = fernet.decrypt(encrypted_data)
    #
    #     return decrypted_data.decode()
    #
    # except Exception as e:
    #     print(f"Ошибка при расшифровке данных: {e}")
        # Не понятно почему не работет декрипт простор ошибка без ошибки. Обновление я не понимаю но ошибка исчеззла нужны тесты # Ошибка в frenet invalid token жебтлы га  разраеье не райзят error по этому было пусто
        #return None
def find_password_for_user(filename=find_path("users.json"),username=""):
    key = load_key()
    with open(filename, 'r') as file:
        data = json.load(file)

    for item in data:
        if item.get("User") == username:
            return item.get("Pass")

    return "Пользователь не найден"

def decrypt_and_save_json(encrypted_file_path=find_path('enc'),key=load_key()):
    key = load_key()
    decrypted_data = decrypt_data()
    output_json_path = str(find_path("enc")[:-4]) + '/users.json'
    # Проверяем, удалось ли расшифровать данные
    if decrypted_data is None:
        log_event("Не удалось расшифровать данные","Warning")
        return

    try:
        # Преобразуем строку в объект Python
        data = json.loads(decrypted_data)

        # Сохраняем объект в файл JSON
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        os.remove(find_path("enc"))
    except json.JSONDecodeError:
            log_event("Ошибка декодирования JSON. Проверьте формат расшифрованных данных.",'Warning',npt=0)
            print("Ошибка при декодировании смотри log")


# Пример использования


# Основная функция
def update_encryption():
    key = load_key()
    # Проверяем, существует ли файл ключа и когда он был создан
    if os.path.exists(key_file):
        key_creation_date = datetime.date.fromtimestamp(os.path.getmtime(key_file))
        if key_creation_date < datetime.date.today():
            # Загружаем старый ключ для расшифровки данных
            old_key = load_key()
            old_data = decrypt_data(old_key)

            # Генерируем новый ключ и перешифровываем данные
            new_key = load_key()
            encrypt_data(old_data, new_key)
            log_event("Данные перешифрованы с новым ключом.")
        else:
            pass
    else:
        # Если ключа нет, генерируем новый и шифруем данные
        new_key = load_key()
        data_to_encrypt = find_path('users.json')
        encrypt_data(data_to_encrypt, new_key)
        log_event("Данные зашифрованы с новым ключом.")

# Хэширвание паролей
def hash_password(pword):
    hashed_password = hashlib.sha256(pword.encode()).hexdigest()
    return hashed_password

def summ_hash(pwrod,user):# Перед передачей паролей, расшифровываем файл
    filename=find_path("users.json")
    hashpwrod=find_password_for_user(username=user,filename=filename)
    if hash_password(pwrod) == hashpwrod:
        return 1
    else:
        return 0

def summ_hash(pwrod,user):# Перед передачей паролей, расшифровываем файл
    filename=find_path("users.json")
    hashpwrod=find_password_for_user(username=user,filename=filename)
    if hash_password(pwrod) == hashpwrod:
        return 1
    else:
        return 0

