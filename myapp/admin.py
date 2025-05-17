from django.contrib import admin

from myapp.models import Category, Task, SubTask # импорт нужных моделей из нужного приложения

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)