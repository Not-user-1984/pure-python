from typing import Dict, List, Optional
from datetime import datetime
import uuid

from dataclasses import dataclass


@dataclass
class Task:
    """Класс для представления задачи."""

    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class TaskManager:
    """Класс для управления задачами в памяти."""

    def __init__(self) -> None:
        """Инициализация пустого хранилища задач."""
        self.tasks: Dict[str, Task] = {}

    def get_all_tasks(self) -> List[Dict]:
        """
        Получить список всех задач.

        Returns:
            List[Dict]: Список словарей, представляющих задачи.
        """
        return [self._task_to_dict(task) for task in self.tasks.values()]

    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        Получить задачу по ID.

        Args:
            task_id (str): Идентификатор задачи.

        Returns:
            Optional[Dict]: Словарь, представляющий задачу, или None, если задача не найдена.
        """
        task = self.tasks.get(task_id)
        if task:
            return self._task_to_dict(task)
        return None

    def create_task(self, title: str, description: str) -> Dict:
        """
        Создать новую задачу.

        Args:
            title (str): Заголовок задачи.
            description (str): Описание задачи.

        Returns:
            Dict: Словарь, представляющий созданную задачу.
        """
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now(),
        )
        self.tasks[task_id] = task
        return self._task_to_dict(task)

    def update_task(self, task_id: str, data: Dict) -> Optional[Dict]:
        """
        Обновить существующую задачу.

        Args:
            task_id (str): Идентификатор задачи для обновления.
            data (Dict): Данные для обновления.

        Returns:
            Optional[Dict]: Обновленная задача или None, если задача не найдена.
        """
        task = self.tasks.get(task_id)
        if not task:
            return None

        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "completed" in data:
            task.completed = data["completed"]

        task.updated_at = datetime.now()
        return self._task_to_dict(task)

    def delete_task(self, task_id: str) -> bool:
        """
        Удалить задачу по ID.

        Args:
            task_id (str): Идентификатор задачи для удаления.

        Returns:
            bool: True, если задача была удалена, иначе False.
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    @staticmethod
    def _task_to_dict(task: Task) -> Dict:
        """
        Преобразовать объект Task в словарь.

        Args:
            task (Task): Объект задачи.

        Returns:
            Dict: Словарь, представляющий задачу.
        """
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
        }
        if task.updated_at:
            task_dict["updated_at"] = task.updated_at.isoformat()
        return task_dict
