from django.contrib import admin
from django.urls import path, include

from apps.common.helpers import schema_view

urlpatterns = [
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('users/', include("apps.users.urls")),
<<<<<<< HEAD
    path('tasks/', include("apps.task.urls")),
    path('comments/', include("apps.comment.urls")),
    path('task/', include("apps.task.urls")),
=======
    path('task/', include("apps.task.urls")),
    path('comments/', include("apps.comment.urls")),
>>>>>>> origin/st_vi

]
