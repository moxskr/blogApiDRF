import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from posts.models import Post


def create_post(title, body, user):
    Post.objects.create(title=title, body=body, created_by=user)


def create_post_params(title, body):
    return {
        'title': title,
        'body': body
    }


@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='qwerty')


@pytest.mark.django_db
def test_get_posts(test_user):
    client = APIClient()

    response = client.get('/blog/posts/')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    response = client.get('/blog/posts/')

    assert response.status_code == 200
    assert len(response.data) == 0

    create_post('test title', 'test body', test_user)

    response = client.get('/blog/posts/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('title') == 'test title'


@pytest.mark.django_db
def test_create_posts(test_user):
    client = APIClient()

    response = client.post('/blog/posts/', create_post_params('test title', 'test body'), format='json')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    response = client.post('/blog/posts/', create_post_params('test title', 'test body'), format='json')

    post = Post.objects.get(title='test title')

    assert response.status_code == 200
    assert response.data.get('title') == 'test title'
    assert response.data.get('body') == 'test body'
    assert post is not None


@pytest.mark.django_db
def test_update_posts(test_user):
    post = Post.objects.create(title='test title', body='test body', created_by=test_user)

    client = APIClient()

    response = client.patch(f'/blog/posts/{post.id}/', create_post_params('test title 2', 'test body 2'), format='json')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    client.patch(f'/blog/posts/{post.id}/', create_post_params('test title 2', 'test body 2'), format='json')

    result_post = Post.objects.get(pk=post.id)

    assert result_post.title == 'test title 2'
    assert result_post.body == 'test body 2'


@pytest.mark.django_db
def test_delete_posts(test_user):
    post = Post.objects.create(title='test title', body='test body', created_by=test_user)

    client = APIClient()

    response = client.delete(f'/blog/posts/{post.id}/')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    client.delete(f'/blog/posts/{post.id}/')

    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(pk=post.id)
