from django.urls import path
from . import views

urlpatterns = [
    path(route="",view=views.home,name="home"),
    path(route="api/get_users",view=views.get_users,name="get_users")
]