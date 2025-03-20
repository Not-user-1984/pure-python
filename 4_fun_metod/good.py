from flask import Flask, request, jsonify
import sqlite3
from typing import Tuple

app = Flask(__name__)


# Класс для работы с БД
class Database:
    def __init__(self, db_name: str = "users.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                             (name TEXT, age INTEGER, email TEXT, city TEXT, country TEXT)""")
            conn.commit()

    def save_user(self, name: str, age: int, email: str, city: str, country: str):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, age, email, city, country) VALUES (?, ?, ?, ?, ?)",
                (name, age, email, city, country),
            )
            conn.commit()

    def get_all_users(self) -> list:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()


# Класс для логирования
class Logger:
    def __init__(self, log_file: str = "log.txt"):
        self.log_file = log_file

    def log(self, message: str):
        with open(self.log_file, "a") as f:
            f.write(f"{message}\n")


def validate_email(email: str) -> bool:
    return "@" in email


def validate_age(age: int) -> bool:
    return age >= 0


def send_welcome_email(email: str, name: str):
    print(f"Sending email to {email}: Welcome {name}!")


# Основная логика приложения
db = Database()
logger = Logger()


@app.route("/user", methods=["GET", "POST"])
def handle_user() -> Tuple[str, int]:
    if request.method == "POST":
        return _handle_post_request(request.get_json())
    return _handle_get_request()


def _handle_post_request(data: dict) -> Tuple[str, int]:
    name = data.get("name", "")
    age = data.get("age", 18)
    email = data.get("email", "")
    city = data.get("city", "Unknown")
    country = data.get("country", "Unknown")
    extra_args = data.get("extra_args", [])
    extra_kwargs = data.get("extra_kwargs", {})

    if not validate_email(email):
        logger.log(f"Invalid email: {email}")
        return jsonify({"error": "Invalid email"}), 400

    if not validate_age(age):
        logger.log(f"Invalid age: {age}")
        return jsonify({"error": "Invalid age"}), 400

    db.save_user(name, age, email, city, country)
    send_welcome_email(email, name)
    logger.log(f"User added: {name}")

    response = {"message": "User added"}
    if extra_args:
        response["extra_args"] = extra_args
    if extra_kwargs:
        response.update(extra_kwargs)

    return jsonify(response), 200


def _handle_get_request() -> Tuple[str, int]:
    users = db.get_all_users()
    logger.log(f"Users fetched: {len(users)}")
    return jsonify(users), 200


if __name__ == "__main__":
    app.run(debug=True)
