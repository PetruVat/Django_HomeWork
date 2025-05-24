from django.db import models
from django.utils.timezone import now

# Create your models here.

status_choises = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Pending", "Pending"),
        ("Blocked", "Blocked"),
        ("Done", "Done")
    ]


class CategoryManager(models.Manager):
    """
    Кастомный менеджер для исключения "мягко" удаленных категорий из запросов.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    """
    Модель для категорий задач.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # Для мягкого удаления
    deleted_at = models.DateTimeField(null=True, blank=True)  # Для хранения времени удаления

    objects = CategoryManager()  # Переопределенный менеджер
    all_objects = models.Manager()  # Менеджер без фильтров

    def delete(self, *args, **kwargs):
        """
        Мягкое удаление — просто обновляем поля вместо удаления из базы.
        """
        self.is_deleted = True
        self.deleted_at = now()
        self.save()

    def restore(self):
        """
        Восстановление мягко удаленной записи.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name




class Task(models.Model):
    title = models.CharField(max_length=50, unique_for_date="deadline")
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=100, choices=status_choises)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "myapp_task"
        verbose_name = "Task"
        unique_together = ("title",)
        ordering = ("-created_at",)


class SubTask(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=status_choises)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "myapp_subtask"
        verbose_name = "SubTask"
        unique_together = ("title",)
        ordering = ("-created_at",)
