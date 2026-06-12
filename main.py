from dataclasses import dataclass, field
from uuid import UUID, uuid4
import json
from datetime import date


@dataclass
class Task:
    title: str
    topshirish_muddati: date
    ustuvorligi: str
    status: bool = field(default_factory=False)
    update_data: date = field(default_factory=date.today)
    id: UUID = field(default_factory=uuid4)
    yaratilgan_vaqti: date = field(default_factory=date.today)


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def delete_task(self, task_id: UUID):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return {"message": "Deleted task"}
        return {"message": "Task not found"}

    def compelete_task(self, task_id: UUID):
        for task in self.tasks:
            if task.id == task_id:
                task.status = True
                return {"message": "Compelete task"}

        return {"message": "Task not found"}

    def ustuvorlik_boyicha_filterlash(self, ustuvorligi: str):
        return {"tasks": [task for task in self.tasks if task.ustuvorligi == ustuvorligi]}

    def status_boyicha_filterlash(self, status: bool):
        return {"status_tasks": [task for task in self.tasks if task.status == status]}

    def kechiktirilgan_vazifalar(self):
        today = date.today()
        return {"kechiktirilgan_vazifalar": [(task, (today - task.topshirish_muddati).days) for task in self.tasks if
                                             task.topshirish_muddati < today]}

    def task_to_dict(self, task: Task):
        return {
            "id": task.id,
            "title": task.title,
            "topshirish_muddati": task.topshirish_muddati,
            "ustuvorligi": task.ustuvorligi,
            "status": task.status,
            "yaratilgan_vaqti": task.yaratilgan_vaqti,
            "update_data": task.update_data
        }

    def save_json(self, task: Task):
        with open("tasks.json", "w") as f:
            json.dump(self.task_to_dict(task), f)

