from flask import Flask, request, jsonify
import sqlite3
import logging
from typing import Tuple

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_name: str = "users.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS users 
                               (name TEXT, age INTEGER, email TEXT, city TEXT, country TEXT)""")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def save_user(self, name: str, age: int, email: str, city: str, country: str):
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute(
                    "INSERT INTO users (name, age, email, city, country) VALUES (?, ?, ?, ?, ?)",
                    (name, age, email, city, country),
                )
        except sqlite3.Error as e:
            logger.error(f"Failed to save user {name}: {e}")
            raise

    def get_all_users(self) -> list:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch users: {e}")
            return []


class ValidationError(Exception):
    pass


def validate_email(email: str) -> None:
    if "@" not in email:
        raise ValidationError("Email must contain '@'")


def validate_age(age: int) -> None:
    if age < 0:
        raise ValidationError("Age cannot be negative")


def send_welcome_email(email: str, name: str):
    logger.info(f"Sending email to {email}: Welcome {name}!")


db = Database()


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

    try:
        validate_email(email)
        validate_age(age)
        db.save_user(name, age, email, city, country)
        send_welcome_email(email, name)
        logger.info(f"User added: {name}")

        response = {"message": "User added"}
        if extra_args:
            response["extra_args"] = extra_args
        if extra_kwargs:
            response.update(extra_kwargs)
        return jsonify(response), 200

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error"}), 500


def _handle_get_request() -> Tuple[str, int]:
    try:
        users = db.get_all_users()
        logger.info(f"Users fetched: {len(users)}")
        return jsonify(users), 200
    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
