from django.contrib import admin
from .models import Task, Comment, Notification

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Notification)



<<<<<<<<< Temporary merge branch 1
=========
# Register your models here.
from apps.task.models import Task, Comment, Notification

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Notification)
>>>>>>>>> Temporary merge branch 2
