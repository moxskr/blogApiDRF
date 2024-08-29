import pytest

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User


@pytest.fixture
def admin_user():
    admin = User.objects.create_superuser('admin', 'qwerty')

    return admin


@pytest.mark.django_db
def test_user_creation():
    client = APIClient()

    client.post('/auth/users/', {'username': 'testuser', 'password': 'qwerty'}, format='json')

    users = User.objects.all()
    tokens = Token.objects.all()

    assert len(users) == 1
    assert len(tokens) == 1


@pytest.mark.django_db
def test_get_users_work_only_for_admin(admin_user):
    client = APIClient()

    response = client.get('/auth/users/')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')

    response = client.get('/auth/users/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_users_work_only_for_admin(admin_user):
    client = APIClient()

    User.objects.create_user(username='user1', password='qwerty')

    response = client.delete('/auth/users/2/')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')

    response = client.delete('/auth/users/2/')

    assert response.status_code == 204


@pytest.mark.django_db
def test_update_users_work_only_for_admin(admin_user):
    client = APIClient()

    user = User.objects.create_user(username='user1', password='qwerty')

    response = client.patch(f'/auth/users/{user.id}/', {'firstname': 'user1'}, format='json')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')

    response = client.patch(f'/auth/users/{user.id}/', {'firstname': 'user1'}, format='json')

    assert response.status_code == 200

    response = client.put(f'/auth/users/{user.id}/', {'username': user.username, 'password': user.password},
                          format='json')

    assert response.status_code == 200
