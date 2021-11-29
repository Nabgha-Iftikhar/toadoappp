"""This module is used to testing the API of todo_app"""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

# Create your tests here.

class GenericTestClass(APITestCase):
    """ class used to login the user
        and access the token authentication """

    def setUp(self) -> None:
        """
        setup the user object, login and token authentication
        :return: None
        """
        self.user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='test@gmail.com',
            username='test',
            password='test'
        )

        login_user_data = {
            'username': 'test',
            'password': 'test'
        }

        url = reverse('login')
        response = self.client.post(
            path=url,
            data=login_user_data,
            format='json'
        )

        token = response.data['access']
        self.headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

        self.task_obj = Task(
            task_title='test2',
            task_description='test2',
            is_complete=False,
            task_category='Home Task',
            task_start_date='2021-11-19T12:02:48.267Z',
            task_end_date='2021-11-19T12:02:48.267Z',
            person=self.user
        )
        self.task_obj.save()


class ForgotPasswordTestCase(GenericTestClass):
    """
    Test Class for testing the Forgot password API
    """

    def setUp(self) -> None:
        """
        Setup user and url for testing the API
        :return: None
        """
        super().setUp()
        self.url = '/api/password_reset/'

    def test_forgot_password(self) -> None:
        """
        Function used to test the forgot password API
        :return: None
        """

        data = {
            "email": "test@gmail.com"
        }

        post_request = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(post_request.status_code, status.HTTP_200_OK)

    def test_unregister_user_forgot_password(self) -> None:
        """
        Test the forgot API with unregister user email
        :return: None
        """

        data = {
            "email": "invalidemail@gmail.com"
        }

        post_request = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(post_request.status_code, status.HTTP_400_BAD_REQUEST)


class RegistrationTestCase(GenericTestClass):
    """
    Test User registration in different cases.
    """

    def setUp(self) -> None:
        """
        Setup the data and url for testing the API
        :return: None
        """
        self.data = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test_user@test.com',
            'username': 'test_user',
            'password': 'Test_user_password_123',
        }
        self.url = '/register/'

    def test_registration(self) -> None:
        """
        Test Registration API
        :return: None
        """
        post_response = self.client.post(
            path=self.url,
            data=self.data
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    def test_already_registered_user(self) -> None:
        """
        Test Register API with already register user
        :return: None
        """

        response = self.client.post(
            path=self.url,
            data=self.data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        again_response = self.client.post(
            path=self.url,
            data=self.data
        )
        self.assertEqual(again_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_invalid_data(self):
        """
        Test register API with invalid data
        :return: None
        """

        invalid_data = {
            'first_name': 123,
            'last_name': 123,
            'email': 123,
            'username': 123,
            'password': 123,
        }

        response = self.client.post(
            path=self.url,
            data=invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTestCase(GenericTestClass):
    """
    Test login api with valid and invalid credentials.
    """

    def setUp(self) -> None:
        """
        Setup the object and url for testing the API
        :return: None
        """
        super().setUp()
        self.url = '/login/'

    def test_login_user(self) -> None:
        """
        Test Login API with valid user
        :return: None
        """

        sample_data = {
            'username': 'test',
            'password': 'test'
        }

        response = self.client.post(
            path=self.url,
            data=sample_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_login(self) -> None:
        """
        Test login API with invalid user login
        :return: None
        """

        invalid_data = {
            'username': '123',
            'password': '123'
        }

        response = self.client.post(
            path=self.url,
            data=invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_user_with_invalid_password(self) -> None:
        """
        Test Login API with valid login and invalid password
        :return:
        """
        sample_data = {
            'username': 'test',
            'password': 'invalid_password'
        }

        response = self.client.post(
            path=self.url,
            data=sample_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_user_with_valid_password(self) -> None:
        """
        Test Login API with invalid login and valid password
        :return: None
        """
        sample_data = {
            "username": "invalid_user",
            "password": "test"
        }

        response = self.client.post(
            path=self.url,
            data=sample_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateTaskTestCases(GenericTestClass):
    """
    Test Create Task API.
    """

    def setUp(self) -> None:
        """
        Setup the object for testing the API
        :return: None
        """

        super().setUp()
        self.data = {
            "task_title": "test",
            "task_description": "test",
            "is_complete": False,
            "task_category": "Home Task",
            "task_start_date": "2021-11-19T12:02:48.267Z",
            "task_end_date": "2021-11-19T12:02:48.267Z"
        }

    def test_create_task(self) -> None:
        """
        Test create Task API
        :return: None
        """

        url = '/tasks/'
        post_response = self.client.post(path=url, data=self.data, **self.headers)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    def test_create_task_with_invalid_data(self) -> None:
        """
        Test create task API with Invalid data
        :return: None
        """

        url = '/tasks/'
        invalid_data = {
            "task_title": 123,
            "task_description": 123,
            "is_complete": 123,
            "task_category": 123,
            "task_start_date": 123,
            "task_end_date": 123
        }
        post_response = self.client.post(path=url, data=invalid_data, **self.headers)
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_invalid_user(self) -> None:
        """
        Test Create Task API with Invalid User
        :return: None
        """
        url = '/tasks/'
        post_response = self.client.post(path=url, data=self.data)
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_without_data(self) -> None:
        """
        Test create task API without data
        :return: None
        """

        url = '/login/'
        post_response = self.client.post(path=url, **self.headers)
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTaskTestCases(GenericTestClass):
    """Class used for testing the Delete Task API"""

    def test_soft_task_delete(self) -> None:
        """
        Soft Delete API Testing
        :return: None
        """
        url = f"/soft_delete/{self.task_obj.pk}/"
        get_response = self.client.delete(path=url, **self.headers)
        self.assertEqual(get_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_id_soft_task_delete(self) -> None:
        """
        Soft delete API testing with invalid task id
        :return: None
        """
        invalid_id = 10
        url = f"/soft_delete/{invalid_id}/"
        get_response = self.client.delete(path=url, **self.headers)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_delete(self) -> None:
        """
        Test Delete Task API
        :return: None
        """
        url = f'/tasks/{self.task_obj.pk}/'
        get_response = self.client.delete(path=url, **self.headers)
        self.assertEqual(get_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_id_task_delete(self) -> None:
        """
        Test Delete Task API with invalid task id
        :return: None
        """
        invalid_id = 10
        url = f'/tasks/{invalid_id}/'
        get_response = self.client.delete(path=url, **self.headers)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)


class CRUDTaskTestCases(GenericTestClass):
    """
    Test get Task, get specific task,
    update task and update specific task.
    """

    def test_get_tasks(self) -> None:
        """
        Test get Tasks API
        :return: None
        """

        url = '/tasks/'
        get_response = self.client.get(path=url, **self.headers)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user_task(self) -> None:
        """
        Test get Tasks API without access token
        :return: None
        """

        url = '/tasks/'
        # header not passed
        get_response = self.client.get(path=url)
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_specific_tasks(self) -> None:
        """
        Test get specific Tasks API
        :return: None
        """

        url = f'/tasks/{self.task_obj.pk}/'
        get_response = self.client.get(path=url, **self.headers)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_get_specific_with_invalid_id(self) -> None:
        """
        Test get Specific Task with invalid id
        :return: None
        """

        # testing with invalid Task ID
        url = f'/tasks/{10}/'
        get_response = self.client.get(path=url, **self.headers)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tasks(self) -> None:
        """
        Test Update Task API
        :return: None
        """
        url = f"/tasks/{self.task_obj.pk}/"
        test_data = {
            "task_title": "updated test",
            "task_description": "updated test",
            "is_complete": True,
            "task_category": "Home Task",
            "task_start_date": "2021-11-22T12:53:32.910Z",
            "task_end_date": "2021-11-22T12:53:32.910Z"
        }

        update_response = self.client.put(path=url, data=test_data, **self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_invalid_id_update_task(self) -> None:
        """
        Test Update Task API with invalid task id
        :return: None
        """
        url = f"/tasks/{10}/"
        test_data = {
            "task_title": "updated test",
            "task_description": "updated test",
            "is_complete": True,
            "task_category": "Home Task",
            "task_start_date": "2021-11-22T12:53:32.910Z",
            "task_end_date": "2021-11-22T12:53:32.910Z"
        }

        update_response = self.client.put(path=url, data=test_data, **self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_task(self) -> None:
        """
        Test partial Update Task API
        :return: None
        """
        url = f"/tasks/{self.task_obj.pk}/"
        test_data = {
            "task_title": "Partial updated test"
        }

        partial_update_response = self.client.patch(path=url, data=test_data, **self.headers)
        self.assertEqual(partial_update_response.status_code, status.HTTP_200_OK)

    def test_invalid_id_partial_update_task(self) -> None:
        """
        Test patch API test with invalid task id
        :return: None
        """
        url = f"/tasks/{10}/"
        test_data = {
            "task_title": "Partial updated test"
        }

        partial_update_response = self.client.patch(path=url, data=test_data, **self.headers)
        self.assertEqual(partial_update_response.status_code, status.HTTP_404_NOT_FOUND)


class ShowUserTestCases(GenericTestClass):
    """Class used for testing the Show Profile API"""

    def test_show_user_profile(self) -> None:
        """
        Test Show User Profile API
        :return: None
        """
        url = "/show_profile/"

        partial_update_response = self.client.get(path=url, **self.headers)
        self.assertEqual(partial_update_response.status_code, status.HTTP_200_OK)

    def test_invalid_user_profile(self) -> None:
        """
        Test Show User Profile API without access Token
        :return: None
        """
        url = "/show_profile/"

        partial_update_response = self.client.get(path=url)
        self.assertEqual(partial_update_response.status_code, status.HTTP_401_UNAUTHORIZED)