import os
import django
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.db.models import ObjectDoesNotExist

# Настройка окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Импорт моделей
from myapp.models import Task, SubTask

# --- Создание записей (Create) ---
def create_tasks():
    try:
        with transaction.atomic():
            # Создание основной задачи
            task = Task.objects.create(
                title="Prepare presentation",
                description="Prepare materials and slides for the presentation",
                status="New",
                deadline=timezone.now() + timedelta(days=3)
            )

            # Создание подзадач
            SubTask.objects.bulk_create([
                SubTask(
                    task=task,
                    title="Gather information",
                    description="Find necessary information for the presentation",
                    status="New",
                    deadline=timezone.now() + timedelta(days=2)
                ),
                SubTask(
                    task=task,
                    title="Create slides",
                    description="Create presentation slides",
                    status="New",
                    deadline=timezone.now() + timedelta(days=1)
                ),
                SubTask(
                    task=task,
                    title="Info",
                    description="Add description",
                    status="Done",
                    deadline=timezone.now() - timedelta(days=3)
                ),
                SubTask(
                    task=task,
                    title="Availability",
                    description="Check availability in stock",
                    status="Done",
                    deadline=timezone.now() - timedelta(days=1)
                ),
            ])
            print("✅ Задача и подзадачи успешно созданы!")
    except Exception as e:
        print(f"❌ Ошибка при создании записей: {e}")


# --- Чтение записей (Read) ---
def read_tasks():
    try:
        print("\n--- Задачи со статусом 'New' ---")
        new_tasks = Task.objects.filter(status="New")
        if new_tasks.exists():
            for task in new_tasks:
                print(f"{task.title} | Deadline: {task.deadline}")
        else:
            print("Нет задач со статусом 'New'.")

        print("\n--- Просроченные подзадачи со статусом 'Done' ---")
        overdue_subtasks = SubTask.objects.filter(status="Done", deadline__lt=timezone.now())
        if overdue_subtasks.exists():
            for subtask in overdue_subtasks:
                print(f"{subtask.title} | Deadline: {subtask.deadline}")
        else:
            print("Нет просроченных подзадач со статусом 'Done'.")
    except Exception as e:
        print(f"❌ Ошибка при чтении записей: {e}")


# --- Изменение записей (Update) ---
def update_tasks():
    try:
        with transaction.atomic():
            task = Task.objects.get(title="Prepare presentation")
            task.status = "In Progress"
            task.save()
            print(f"✅ Статус задачи '{task.title}' изменен на '{task.status}'")

            subtask1 = SubTask.objects.get(title="Gather information")
            subtask1.deadline = timezone.now() - timedelta(days=2)
            subtask1.save()
            print(f"✅ Срок подзадачи '{subtask1.title}' изменен на {subtask1.deadline}")

            subtask2 = SubTask.objects.get(title="Create slides")
            subtask2.description = "Create and format presentation slides"
            subtask2.save()
            print(f"✅ Описание подзадачи '{subtask2.title}' изменено.")
    except ObjectDoesNotExist as e:
        print(f"❌ Объект не найден: {e}")
    except Exception as e:
        print(f"❌ Ошибка при изменении записей: {e}")


# --- Удаление записей (Delete) ---
def delete_tasks():
    try:
        with transaction.atomic():
            task = Task.objects.get(title="Prepare presentation")
            task.delete()
            print(f"✅ Задача '{task.title}' и все связанные подзадачи удалены.")
    except ObjectDoesNotExist:
        print("❌ Задача не найдена для удаления.")
    except Exception as e:
        print(f"❌ Ошибка при удалении записей: {e}")
