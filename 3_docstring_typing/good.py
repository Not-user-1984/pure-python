"""
Пример Flask-приложения для управления простым API списка задач.

Это приложение демонстрирует создание RESTful API с использованием Flask,
включая аннотации типов, документацию и соблюдение стиля кодирования PEP 8.

Приложение предоставляет следующие конечные точки:
- GET /tasks - получить список всех задач
- GET /tasks/<task_id> - получить задачу по ID
- POST /tasks - создать новую задачу
- PUT /tasks/<task_id> - обновить существующую задачу
- DELETE /tasks/<task_id> - удалить задачу

Запуск приложения:
    $ python app.py
"""

from flask import Flask, request, jsonify, Response
from typing import Tuple
from data_task import TaskManager

import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Создание Flask-приложения
app = Flask(__name__)
task_manager = TaskManager()


@app.route("/tasks", methods=["GET"])
def get_tasks() -> Response:
    """Получить список всех задач."""
    tasks = task_manager.get_all_tasks()
    return jsonify(tasks)


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id: str) -> Tuple[Response, int]:
    """Получить конкретную задачу по ID."""
    task = task_manager.get_task(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks", methods=["POST"])
def create_task() -> Tuple[Response, int]:
    """Создать новую задачу."""
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    task = task_manager.create_task(data["title"], data["description"])
    return jsonify(task), 201


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id: str) -> Tuple[Response, int]:
    """Обновить существующую задачу."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    task = task_manager.update_task(task_id, data)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id: str) -> Tuple[Response, int]:
    """Удалить задачу."""
    if task_manager.delete_task(task_id):
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
    logger.info("Приложение запущено на http://127.0.0.1:5000/")
