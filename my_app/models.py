from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class TodoItem(models.Model):
    item_name = models.CharField(max_length=100)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ('item_name',)
