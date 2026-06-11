from dataclasses import dataclass, field
import json
from datetime import date
from uuid import uuid4, UUID


@dataclass
class Task:
    title: str
    topshirish_muddati: date
    ustuvorligi: str
    status: bool
    update_date: date
    yaratilgan_vaqti: date = field(default_factory=date.today)
    id: UUID = field(default_factory=uuid4)


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)
        return {"message": "Task Added"}

    def delete_task(self, task_id: str):
        for i in self.tasks:
            if i.id == task_id:
                self.tasks.remove(i)
                return {"message": "Task Removed"}
        return {"message": "Task Not Found"}

    def complete_task(self, task_id: str):
        for i in self.tasks:
            if i.id == task_id:
                i.status = True
                i.update_date = date.today()
                return {"message": "Task Updated"}

        return {"message": "Task Not Found"}

    def filter_by_ustuvorligi(self, ustuvorligi: str):
        return {"tasks": (i for i in self.tasks if i.ustuvorligi == ustuvorligi)}

    def filter_by_status(self, status: bool):
        return {"tasks": (i for i in self.tasks if i.status == status)}

    def kechikkan_tasks(self):
        today = date.today()
        return {"kechikan_tasks": [
            (i, (today - i.topshirish_muddati).days)
            for i in self.tasks
            if i.topshirish_muddati and i.topshirish_muddati < today

        ]}

    def task_to_dict(self, task: Task):
        return {
            "id": str(task.id),
            "title": task.title,
            "topshirish_muddati": str(task.topshirish_muddati),
            "ustuvorligi": str(task.ustuvorligi),
            "status": str(task.status),
            "update_date": str(task.update_date),
            "yaratilgan_vaqti": str(task.yaratilgan_vaqti)}
