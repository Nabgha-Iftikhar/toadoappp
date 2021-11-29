"""this module is used to url management of todo_app"""
from django.urls import path
from . import views

APP_NAME = 'TODO_API'
urlpatterns = [  # pylint: disable=C0103
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('soft_delete/<int:pk>/', views.SoftDeleteTaskView.as_view(), name='delete_task'),
    path('show_profile/', views.ShowUserProfileView.as_view(), name='show_profile'),
]