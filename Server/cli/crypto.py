import os
from cryptography.fernet import Fernet
import datetime
from Scripts.modules import *
from Scripts.log import log_event
import json
# Путь к файлу с ключом
key_file = find_path(nroot=1)+"/Server/Users/db/key"

# Путь к файлу с данными


# Функция для генерации и сохранения нового ключа
def generate_and_save_key():
    key = Fernet.generate_key()
    with open(key_file, 'wb') as file:
        file.write(key)
    return key

# Функция для загрузки ключа из файла
def load_key():
    with open(key_file, 'rb') as file:
        return file.read()
key=load_key()
# Функция для шифрования данных
def encrypt_data(file_path=find_path("users.json")):
    fernet = Fernet(key)

    try:
        with open(file_path, 'r') as file:
            data = file.read()
        encrypted_data = fernet.encrypt(data.encode())

        with open(file_path[:-11]+'/enc', 'wb') as file:
            file.write(encrypted_data)
        os.remove(find_path('users.json'))
    except Exception as e:
        print(f"Произошла ошибка при шифровании данных: {e}")

# Функция для расшифровки данных
def decrypt_data(file_path=find_path(nroot=1)+'/Server/Users/db/enc'):
    # Создаем объект Fernet с предоставленным ключом
    fernet = Fernet(key)

    # Читаем зашифрованные данные из файла
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    # Расшифровываем данные и возвращаем их
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data.decode()
    except Exception as e:
        print(f"Ошибка при расшифровке данных: {e}")
        return None


def decrypt_and_save_json(encrypted_file_path=find_path('enc'),key=load_key()):
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

        log_event("Данные успешно сохранены")
        os.remove(find_path("enc"))
    except json.JSONDecodeError:
            log_event("Ошибка декодирования JSON. Проверьте формат расшифрованных данных.",'Warning',npt=0)
            print("Ошибка при декодировании смотри log")


# Пример использования


# Основная функция
def update_encryption():
    # Проверяем, существует ли файл ключа и когда он был создан
    if os.path.exists(key_file):
        key_creation_date = datetime.date.fromtimestamp(os.path.getmtime(key_file))
        if key_creation_date < datetime.date.today():
            # Загружаем старый ключ для расшифровки данных
            old_key = load_key()
            old_data = decrypt_data(old_key)

            # Генерируем новый ключ и перешифровываем данные
            new_key = generate_and_save_key()
            encrypt_data(old_data, new_key)
            log_event("Данные перешифрованы с новым ключом.")
        else:
            pass
    else:
        # Если ключа нет, генерируем новый и шифруем данные
        new_key = generate_and_save_key()
        data_to_encrypt = find_path('users.json')
        encrypt_data(data_to_encrypt, new_key)
        log_event("Данные зашифрованы с новым ключом.")

# Запуск функции
decrypt_and_save_json()