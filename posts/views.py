from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Comment
from posts.serializers import PostSerializer, PostDetailSerializer, CommentSerializer


class PostsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        serializer = PostDetailSerializer(post)

        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        deserializer = PostSerializer(data=request.data)

        if deserializer.is_valid(raise_exception=True):
            post = deserializer.save()

            post.created_by = request.user

            post.save()

            serializer = PostSerializer(post)

            return Response(data=serializer.data)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_pk']

        return Comment.objects.filter(post_id=post_id)

    def create(self, request, post_pk=None, *args, **kwargs):
        deserializer = CommentSerializer(data=request.data)

        if deserializer.is_valid(raise_exception=True):
            post = Post.objects.get(pk=post_pk)

            comment = deserializer.save()

            comment.created_by = request.user
            comment.post = post

            comment.save()

            serializer = CommentSerializer(comment)

            return Response(data=serializer.data)
