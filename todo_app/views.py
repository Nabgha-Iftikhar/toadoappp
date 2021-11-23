from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import AdminRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer, UserSerializer,  ChangePasswordSerializer


class TaskViewSet(viewsets.ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = [AdminRenderer, JSONRenderer]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset

    def perform_create(self, serializer):
        user = User.objects.get(username=self.request.user)
        return serializer.save(user=user)

    def get(self, request, format=None):
        task = Task.objects.all()
        serializer = UserSerializer(task, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        self.http_method_names.append("GET")

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TaskCreate(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     renderer_classes = [BrowsableAPIRenderer]
#
# #
# # class TaskList(generics.ListAPIView):
# #     queryset = Task.objects.all()
# #     serializer_class = TaskSerializer
# #
# #
# # class TaskUpdate(generics.RetrieveUpdateAPIView):
# #     queryset = Task.objects.all()
# #     serializer_class = TaskSerializer
#
#
# class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer

#
# @api_view(["GET"])
# def taskList(request):
#     tasks = Task.objects.all()
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)
#
#
# @api_view(["GET"])
# def taskDetail(request, pk):
#     tasks = Task.objects.get(id=pk)
#     serializer = TaskSerializer(tasks, many=False)
#     return Response(serializer.data)
#
#
# @api_view(["POST"])
# def taskCreate(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# @api_view(["POST"])
# def taskUpdate(request, pk):
#     task = Task.objects.get(id=pk)
#     serializer = TaskSerializer(instance=task, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# @api_view(["POST"])
# def taskUpdate(request, pk):
#     task = Task.objects.get(id=pk)
#     task.delete()
#     return Response('Items successfully deleted')
