from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from posts.views import PostsViewSet, CommentsViewSet

router = SimpleRouter()

router.register(r'posts', PostsViewSet)

posts_router = NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentsViewSet, basename='post-comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
]