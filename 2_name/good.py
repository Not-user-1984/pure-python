from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def home_page():
    """Отображает главную страницу приложения."""
    html = "<h1>Добро пожаловать</h1><p>Это главная страничка</p>"
    return html


@app.route("/submit", methods=["POST"])
def submit_form():
    """Обрабатывает данные формы и возвращает результат."""
    name = request.form["name"]
    age = request.form["age"]
    if age.isdigit():
        age = int(age)
    else:
        age = 0
    server_response = f"{name} {age}"
    return render_template("result.html", response=server_response)


@app.route("/api/data")
def get_data():
    """Возвращает данные в формате JSON через API."""
    data = {
        "user": "ivan",
        "age": 25,
        "city": "moscow",
    }
    return jsonify(data)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Обрабатывает регистрацию пользователя."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if len(username) > 3 and len(password) > 6:
            message = f"Успех для {username} с {email}"
            return message
        return "Ошибка в данных"
    return render_template("register.html")


@app.route("/calc")
def calculate():
    """Выполняет простые вычисления и возвращает результат."""
    x = 10
    y = 20
    z = x + y * 2
    result = f"Итог: {z}"
    return result


@app.route("/long_func")
def long_function():
    """Выполняет несколько вычислений и возвращает результат."""
    number_one = 5
    number_two = 10
    sum_result = number_one + number_two
    difference = number_one - number_two
    product = number_one * number_two
    server_response = (
        f"Сумма: {sum_result}, Разность: {difference}, Произведение: {product}"
    )
    return server_response


@app.route("/about")
def about_page():
    """Отображает страницу 'О нас'."""
    text = "Это страница о нас"
    return text


@app.route("/error")
def error_handler():
    """Обрабатывает и возвращает сообщение об ошибке."""
    status = "Ошибка сервера"
    return status


if __name__ == "__main__":
    app.run(debug=True)
