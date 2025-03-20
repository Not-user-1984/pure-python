from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# LBYL подход и print вместо логирования
class Database:
    def save_user(self, name, age, email, city, country):
        conn = sqlite3.connect('users.db')
        if conn is not None:  # LBYL: проверка перед использованием
            cursor = conn.cursor()
            if cursor is not None:
                cursor.execute("INSERT INTO users (name, age, email, city, country) VALUES (?, ?, ?, ?, ?)",
                              (name, age, email, city, country))
                conn.commit()
        conn.close()

    def get_all_users(self):
        conn = sqlite3.connect('users.db')
        if conn is not None:
            cursor = conn.cursor()
            if cursor is not None:
                cursor.execute("SELECT * FROM users")
                return cursor.fetchall()
        conn.close()
        return []

def validate_email(email):
    if '@' in email:  # LBYL
        return True
    return False

@app.route('/user', methods=['POST'])
def handle_user():
    data = request.get_json()
    name = data.get('name', '')
    age = data.get('age', 18)
    email = data.get('email', '')
    city = data.get('city', 'Unknown')
    country = data.get('country', 'Unknown')

    if not validate_email(email):  # LBYL
        print(f"Invalid email: {email}")
        return jsonify({"error": "Invalid email"}), 400
    
    if age >= 0:  # LBYL
        db = Database()
        db.save_user(name, age, email, city, country)
        print(f"User {name} added, sending email to {email}")
        return jsonify({"message": "User added"}), 200
    else:
        print(f"Invalid age: {age}")
        return jsonify({"error": "Invalid age"}), 400

if __name__ == '__main__':
    app.run(debug=True)