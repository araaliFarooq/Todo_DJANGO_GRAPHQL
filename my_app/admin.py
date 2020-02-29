from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import TodoItem, TodoList

# Register your models here.
admin.site.unregister(get_user_model())
admin.site.register(get_user_model())
admin.site.register(TodoList)
admin.site.register(TodoItem)
