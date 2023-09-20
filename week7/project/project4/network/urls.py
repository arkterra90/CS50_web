
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post", views.post, name="post"),
    path("register", views.register, name="register"),
    path("<int:user_id>/user", views.user, name="user"),
    path("<int:user_id>/follow", views.follow, name="follow"),
    # API Route for follow button
    path("follow", views.follow, name="compose")

    ]
