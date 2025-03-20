from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def home_page():
    """Отображает главную страницу приложения."""
    html = "<h1>Добро пожаловать на сайт</h1><p>Это главная страница приложения на Flask</p>"
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
    result = f"{name} {age}"
    return render_template("result.html", result=result)


@app.route("/api/data")
def get_data():
    """Возвращает данные в формате JSON через API."""
    data = {
        "user": "Иван",
        "age": 25,
        "city": "Москва",
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
            return f"Регистрация успешна для {username} с email {email}"
        return "Ошибка: короткое имя или пароль"
    return render_template("register.html")


@app.route("/longexample")
def long_example():
    """Пример длинной функции с вычислениями и выводом результата."""
    x = 10
    y = 20
    result = x + y
    print(
        "нарушение: длинная строка, нет пробела после оператора"
        "нарушение: длинная строка, нет пробела после оператора"
        "нарушение: длинная строка, нет пробела после оператора"
        "нарушение: длинная строка, нет пробела после оператора"
    )
    return f"Выполнено:{result} "
