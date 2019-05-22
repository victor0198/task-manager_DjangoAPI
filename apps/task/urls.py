from django.urls import path
from apps.task.views import CompletedTaskListView, DeleteView, AddTaskView, AddTaskSelfView, UpdateTaskState, \
    TaskCommentsView, UserTaskView, FilterTask, TaskItemCommentsView, UpdateTask, TaskViewSet, \
    TaskFilterStatusCreatedViewSet, TaskFilterStatusInprocessViewSet, TaskFilterStatusFinishedViewSet, \
    TaskSearchViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', TaskViewSet, base_name='all_tasks')
router.register(r'created', TaskFilterStatusCreatedViewSet, base_name='task_list_status')
router.register(r'open', TaskFilterStatusInprocessViewSet, base_name='task_list_status')
router.register(r'closed', TaskFilterStatusFinishedViewSet, base_name='task_list_status')
router.register(r'search', TaskSearchViewSet, base_name='all_tasks')
urlpatterns = router.urls

urlpatterns += [
    # path('list_task/<str:status>/', TaskFilterStatusView.as_view(), name='task_list'),

    path('completed_task/', CompletedTaskListView.as_view(), name='completed_list'),
    path('delete_task/<int:pk>/', DeleteView.as_view(), name='delete_task'),
    path('create/', AddTaskView.as_view(), name='task_create'),
    path('create_self/', AddTaskSelfView.as_view(), name='task_create_self'),
    path('task_details/<int:pk>/', TaskItemCommentsView.as_view(), name='task_item'),
    path('task_update/', UpdateTask.as_view(), name="update_task"),

    path('<int:pk>/', TaskCommentsView.as_view(), name='tasks_all_details'),
    path('my_tasks/', UserTaskView.as_view(), name='all_task_user'),
    path('update_status/', UpdateTaskState.as_view(), name="update_status"),
    path('task_all_filter/', FilterTask.as_view(), name="filter_task"),

]

for i in range(1, 4):
    del urlpatterns[1]
for i in range(1, 4):
    del urlpatterns[2]
for i in range(1, 4):
    del urlpatterns[3]

# for n in range(10):
#     for i in range(1, 4):
#         del urlpatterns[n]
# print(urlpatterns)
