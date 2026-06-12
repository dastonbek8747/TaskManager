from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import date
from enum import Enum
import json
import os


class Priority(str, Enum):
    HIGH   = "Yuqori"
    MEDIUM = "O'rta"
    LOW    = "Past"

    _order = {"Yuqori": 3, "O'rta": 2, "Past": 1}

    def __lt__(self, other: "Priority") -> bool:
        return self._order[self.value] < self._order[other.value]


@dataclass
class Task:
    title:      str
    deadline:   date
    priority:   Priority
    status:     bool = False
    id:         UUID = field(default_factory=uuid4)
    created_at: date = field(default_factory=date.today)
    updated_at: date = field(default_factory=date.today)

    def __str__(self):
        done = "✅" if self.status else "⏳"
        return f"{done} [{self.priority.value}] {self.title} — {self.deadline}"

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, priority={self.priority}, deadline={self.deadline})"

    def __lt__(self, other: "Task"):
        return self.priority > other.priority

    def to_dict(self):
        return {
            "id":         str(self.id),
            "title":      self.title,
            "deadline":   self.deadline.isoformat(),
            "priority":   self.priority.value,
            "status":     self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title    = data["title"],
            deadline = date.fromisoformat(data["deadline"]),
            priority = Priority(data["priority"]),
            status   = data["status"],
        )
        task.id         = UUID(data["id"])
        task.created_at = date.fromisoformat(data["created_at"])
        task.updated_at = date.fromisoformat(data["updated_at"])
        return task


JSON_FILE = "tasks.json"


class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []
        self.load_json()

    def add_task(self, title: str, deadline: date, priority: Priority) -> Task:
        task = Task(title=title, deadline=deadline, priority=priority)
        self.tasks.append(task)
        self.save_json()
        return task

    def complete_task(self, task_id: UUID) -> dict:
        task = self._find(task_id)
        if not task:
            return {"ok": False, "message": "Vazifa topilmadi"}
        task.status     = True
        task.updated_at = date.today()
        self.save_json()
        return {"ok": True, "message": "Bajarildi ✅"}

    def delete_task(self, task_id: UUID) -> dict:
        task = self._find(task_id)
        if not task:
            return {"ok": False, "message": "Vazifa topilmadi"}
        self.tasks.remove(task)
        self.save_json()
        return {"ok": True, "message": "O'chirildi 🗑️"}

    def filter_by_priority(self, priority: Priority):
        return (t for t in self.tasks if t.priority == priority)

    def filter_by_status(self, done: bool):
        return (t for t in self.tasks if t.status == done)

    def overdue_tasks(self) -> list[tuple[Task, int]]:
        today = date.today()
        return [
            (t, (today - t.deadline).days)
            for t in self.tasks
            if t.deadline < today and not t.status
        ]

    def stats(self) -> dict:
        total   = len(self.tasks)
        done    = sum(1 for t in self.tasks if t.status)
        overdue = len(self.overdue_tasks())
        return {"total": total, "done": done, "overdue": overdue, "active": total - done}

    def save_json(self):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tasks], f, ensure_ascii=False, indent=2)

    def load_json(self):
        if not os.path.exists(JSON_FILE):
            return
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                self.tasks = [Task.from_dict(item) for item in json.load(f)]
        except (json.JSONDecodeError, KeyError):
            self.tasks = []

    def _find(self, task_id: UUID) -> Task | None:
        return next((t for t in self.tasks if t.id == task_id), None)