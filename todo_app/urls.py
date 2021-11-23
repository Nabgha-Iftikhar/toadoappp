from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'task-view', views.TaskViewSet, basename='task-view')
urlpatterns = [
    path('', include(router.urls)),
    path('register-user', views.CreateUserView.as_view(), name='register'),

    ]