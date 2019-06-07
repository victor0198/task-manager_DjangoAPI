from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.users.views import UserSearchViewSet, RegisterUserView, MeDetails
from apps.time_tracker.views import LoggedTimeView, LogChartView

router = DefaultRouter()
router.register(r'search', UserSearchViewSet, base_name='all_users')
urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeDetails.as_view(), name='user_me'),
    path('logged_time/<int:pk>/', LoggedTimeView.as_view(), name="logged"),
    path('statistics/<int:pk>/', LogChartView.as_view(), name="logged"),

]

for i in range(1, 4):
    del urlpatterns[1]
