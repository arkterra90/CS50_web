from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list_add", views.list_add, name="list_add"),
    path("<int:list_id>", views.list_view, name="list_view"),
    path("<int:list_id>/item_comments", views.item_comments, name="item_comments"),
    path('<int:list_id>/bid_place', views.bid_place, name='bid_place'),
    path('<int:list_id>/watch_form', views.watch_list, name='watch_list')
]
