import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from posts.models import Post, Comment


def create_comment(body, post, user):
    return Comment.objects.create(body=body, post=post, created_by=user)


@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='qwerty')


@pytest.fixture
def test_post(test_user):
    return Post.objects.create(title='test post', body='test body', created_by=test_user)

@pytest.mark.django_db
def test_get_comments(test_user, test_post):
    client = APIClient()

    response = client.get(f'/blog/posts/{test_post.id}/comments/')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    response = client.get(f'/blog/posts/{test_post.id}/comments/')

    assert response.status_code == 200
    assert len(response.data) == 0

    create_comment('test comment', test_post, test_user)

    response = client.get(f'/blog/posts/{test_post.id}/comments/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('body') == 'test comment'


@pytest.mark.django_db
def test_create_comments(test_user, test_post):
    client = APIClient()

    response = client.post(f'/blog/posts/{test_post.id}/comments/', {'body': 'test comment'}, format='json')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    response = client.post(f'/blog/posts/{test_post.id}/comments/', {'body': 'test comment'}, format='json')

    comment = Comment.objects.get(body='test comment')

    assert response.status_code == 200
    assert comment is not None


@pytest.mark.django_db
def test_update_comments(test_user, test_post):
    client = APIClient()

    comment = create_comment('test comment', test_post, test_user)

    response = client.patch(f'/blog/posts/{test_post.id}/comments/{comment.id}/', {'body': 'test comment 2'}, format='json')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    response = client.patch(f'/blog/posts/{test_post.id}/comments/{comment.id}/', {'body': 'test comment 2'}, format='json')

    result_comment = Comment.objects.get(pk=comment.id)

    assert response.status_code == 200
    assert result_comment.body == 'test comment 2'


@pytest.mark.django_db
def test_delete_comments(test_user, test_post):
    client = APIClient()

    comment = create_comment('test comment', test_post, test_user)

    response = client.patch(f'/blog/posts/{test_post.id}/comments/{comment.id}/')

    assert response.status_code == 401

    client.credentials(HTTP_AUTHORIZATION=f'Token {test_user.auth_token}')

    client.delete(f'/blog/posts/{test_post.id}/comments/{comment.id}/')

    with pytest.raises(comment.DoesNotExist):
        Comment.objects.get(pk=comment.id)




