from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:title>', views.page, name="page"),
    path("newpage", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("random", views.random_page, name="random")
]
