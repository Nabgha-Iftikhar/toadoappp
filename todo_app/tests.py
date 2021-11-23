import pytest
import coreapi
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token, AccessToken
from rest_framework.test import APITestCase, APIClient
from .models import User, Task


@pytest.mark.django_db
class RegistrationTestCase(APITestCase):
    """
    Test User Registration In different cases.
    """

    def test_registration(self):
        data = {
            "first_name": "nabgha1",
            "last_name": "iftikhar",
            "username": "nabgha",
            "password": "123",
            "email": "iftikharnabgha93@gmail.com",
        }
        # data1 = {
        #     'first_name': 'test',
        #     'last_name': 'test',
        #     'email': 'test_user@test.com',
        #     'username': 'test_user',
        #     'password': '123',
        # }

        url = '/register-user'
        response1 = self.client.post(url, data)
        response2 = self.client.post(url, data)
        # response3 = self.client.post(url, data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTestCase(APITestCase):
    """
    Test login api with valid and invalid credentials.
    """

    def setUp(self) -> None:
        user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='test@gmail.com',
            username='test',
            password='test123456'
        )

    def test_login_user(self):
        url = '/api/login /'
        data = {
            'username': 'test',
            'password': 'test123456'
        }
        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        data1 = {
            'username': 'test',
            'password': 'test'
        }
        response2 = self.client.post(url, data1)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)


class ViewTaskTestCase(APITestCase):
    """
    Test View task on different conditions.
    """

    def setUp(self) -> None:
        """
        Setup required things for task creating i.e user.
        """
        user = User.objects.create_user(
            first_name='nabghaiftikhar',
            last_name='kamboh',
            email='iftikharnabgha93@.com',
            username='Nabgha',
            password='12345'

        )
        data1 = {
            'username': 'test',
            'password': 'test1234'
        }
        url = '/api/login /'
        response = self.client.post(url, {'username': 'Nabgha', 'password': '12345'}, format='json')

        self.token = response.data['access']

        response = self.client.post('/api/login /', data1)

    def test_viewtask(self):
        headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }
        response = self.client.get(path='/task-view/', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)



@pytest.mark.django_db
class TaskTestCase(APITestCase):
    """
    Test employee Creation
    """

    def setUp(self) -> None:
        """
        Setup required things for employee creating i.e user.
        """

        self.user = User.objects.create_user(
            first_name='nabghaiftikhar',
            last_name='kamboh',
            email='iftikharnabgha93@test.com',
            username='Nabgha',
            password='12345'

        )

        self.user.save()
        data1 = {
            'username': 'test',
            'password': 'test1234'
        }
        url = '/api/login /'
        response = self.client.post(url, {'username': 'Nabgha', 'password': '12345'}, format='json')

        self.token = response.data['access']

        response = self.client.post('/api/login /', data1)


        # data = {
        #     'username': 'nabgha',
        #     'password': '123'
        # }
        #
        # response = self.client.login(username='pakiza', password='pakiza1234')
        url = '/api/login /'
        resp = self.client.post(url, {'username': 'Nabgha', 'password': '12345'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.token = resp.data['access']

        self.headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }


        # positions = Position.objects.create(
        #     title='PHP Developer')
        # positions.save()
    #

    def test_task_delete(self):
        """
        #         Tasks retrieve.
        #         """
        #

        data4 = Task(
            # "user": self.user.pk,
            title="saya",
            description="lawn",
            complete=True,
            user=self.user,

        )
        data4.save()
        url = f'/task-view/{data4.id}/'
        print(url)
        req = self.client.delete(url, **self.headers)

        #
        self.assertEqual(req.status_code, status.HTTP_303_SEE_OTHER)


    def test_create_task(self):

        data = {
            # "user": self.user.pk,
              "title": "saya",
              "description": "lawn",
              "complete": True,
              "user": self.user.pk,

        }
        url = '/task-view/'
        response = self.client.post(path=url, data=data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_list(self):
        """
        #         Employees retrieve.
        #         """
        #

        url = '/task-view/'
        req = self.client.get(url, **self.headers)



        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def test_task_retrieve(self):
        user_id = self.user.pk
        """
        #         Tasks retrieve.
        #         """
        data = Task(
            # "user": self.user.pk,
            title= "saya",
            description= "lawn",
            complete= True,
            user= self.user,


        )
        data.save()

        response = self.client.get(f'/task-view/{data.id}/' , **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_update(self):
        """
        #         Tasks retrieve.
        #         """
        #

        data = Task(
            # "user": self.user.pk,
            title="saya",
            description="lawn",
            complete=True,
            user=self.user,

        )
        data.save()
        data1 = {
            # "user": self.user.pk,
            "title": "saya",
            "description": "lawn",
            "complete": True,
            "user": self.user.pk,

        }
        url = f'/task-view/{data.id}/'
        print(url)
        req = self.client.put(url, data1, **self.headers)
        print(req.data)
        req_task = req.data

        #
        self.assertEqual(req.status_code, status.HTTP_200_OK)
    def test_forgot_password(self):
        user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='test@gmail.com',
            username='test',
            password='test1234'
        )
        url = '/api/password_reset/'
        data1 = {
            "email": "test@gmail.com"
        }
        data2 = {
            "email": "iftikharnabgha93@gmail.com"
        }
        response1 = self.client.post(url, data1)
        response2 = self.client.post(url, data2)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
