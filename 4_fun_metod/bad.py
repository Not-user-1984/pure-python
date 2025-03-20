from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)

@app.route('/user', methods=['GET', 'POST'])
def handle_user():
    # Одна большая функция делает всё
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        age = data['age']
        email = data['email']
        city = data.get('city')
        country = data.get('country')
        extra_info = data.get('extra_info')
        
        # Валидация, логика и работа с БД в одном месте
        if '@' not in email:
            with open('log.txt', 'a') as f:
                f.write(f"Invalid email: {email}\n")
            return "Invalid email", 400
        
        if age < 0:
            with open('log.txt', 'a') as f:
                f.write(f"Invalid age: {age}\n")
            return "Invalid age", 400
        
        # Изменение глобального состояния
        global last_user
        last_user = name
        
        # Сохранение в БД
        cursor.execute(f"INSERT INTO users (name, age, email, city, country) VALUES ('{name}', {age}, '{email}', '{city}', '{country}')")
        conn.commit()
        
        # Логирование
        with open('log.txt', 'a') as f:
            f.write(f"User added: {name}, extra_info: {extra_info}\n")
        
        # Отправка "email" (имитация)
        print(f"Sending email to {email}: Welcome {name}!")
        
        return json.dumps({"message": "User added", "extra": extra_info})
    
    else:
        # Обработка GET-запроса
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        
        with open('log.txt', 'a') as f:
            f.write(f"Users fetched: {len(users)}\n")
        
        print(f"Returning {len(users)} users")
        return json.dumps(users)

if __name__ == '__main__':
    # Создание таблицы (тоже часть основной логики)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (name TEXT, age INTEGER, email TEXT, city TEXT, country TEXT)''')
    conn.commit()
    conn.close()
    
    global last_user
    last_user = ""
    app.run(debug=True)