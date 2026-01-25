from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(route="",view=views.home,name="home"),
    path(route="api/get_users",view=views.get_users,name="get_users"),
    path(route="api/get_my_attendances",view=views.get_my_attendance,name="get_my_attendance"),
path(route="api/get_all_sessions",view=views.get_all_sessions,name="get_all_sessions"),
path(route="api/get_today_sessions",view=views.get_today_sessions,name="get_today_sessions"),
    path(route="api/get_teacher_data",view=views.get_teacher_data,name="get_teacher_data"),

    path(route="api/register",view=views.register_user, name='register'),


    path(route='api/login',view=views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(route='api/logout',view=views.LogoutView.as_view(),name='logout'),
    path(route='api/token/refresh',view=TokenRefreshView.as_view(), name='token_refresh'),
]