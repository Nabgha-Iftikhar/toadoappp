"""This module is used to create API for Todo_app"""
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, viewsets, status
from rest_framework.renderers import JSONRenderer, AdminRenderer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .models import Task
from .serializers import CreateUserSerializer, TaskSerializer


# Create your views here.

def get_tasks() -> Task:
    """
    get the list of all Tasks
    :return:
    """
    return Task.objects.all()  # pylint: disable= E1101


class CreateListTaskView(viewsets.ModelViewSet):  # pylint: disable=R0901
    """
    ViewSet for CRUD API's
    """
    serializer_class = TaskSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        """
        Message: Create new task
        Parameters:
            request: Request from user for task creation
        Returns:
            Response:
        """
        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = valid_data['user_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(pk=user)
        serializer.validated_data['person'] = user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self) -> Task:
        """
        queryset function to filter the specific task of user
        :return: Task
        """
        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        tasks = get_tasks().filter(person=valid_data['user_id'], is_complete=False)
        self.queryset = tasks
        return tasks


class RegisterUser(generics.CreateAPIView):
    """
    CreateAPIView for Registration of user
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, AdminRenderer]


class SoftDeleteTaskView(generics.DestroyAPIView):
    """ DestroyAPIView for Soft Delete of user """
    queryset = get_tasks().filter(is_complete=False)

    def delete(self, request, *args, **kwargs) -> Response:
        """
        Soft Delete the task of user
        :param request: POST Request
        :param args: Extra arguments
        :param kwargs: Extra keyword arguments
        :return: Response
        """
        instance = self.get_object()
        instance.is_complete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowUserProfileView(generics.ListAPIView):
    """ ListAPIView for show the Profile of user"""
    serializer_class = CreateUserSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self) -> User:
        """
        queryset function to filter the specific user profile
        :return: User
        """
        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = User.objects.filter(pk=valid_data['user_id'])
        return user.order_by('id')