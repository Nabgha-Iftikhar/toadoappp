""" This module is used to serialize the api data"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class CreateUserSerializer(serializers.ModelSerializer):
    """
    User Serializer class to serialize the user data for login & email.
    """

    class Meta:  # pylint: disable=R0903
        """
        Class used to enhance user serialize class functionality
        """
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'style': {'input_type': 'password'}, 'write_only': True}}
        write_only_fields = ('person',)


class TaskSerializer(serializers.ModelSerializer):
    """
    Task Serializer class to serialize the Task data for CRUD operations.
    """

    class Meta:  # pylint: disable=R0903
        """
        Class used to enhance Task serialize class functionality
        """
        model = Task
        fields = ['task_title', 'task_description', 'is_complete', 'task_category',
                  'task_start_date', 'task_end_date', 'person']
        read_only_fields = ('person',)