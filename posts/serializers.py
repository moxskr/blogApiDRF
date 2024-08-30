from rest_framework import serializers

from posts.models import Post, Comment
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_by', 'created_date', 'last_modified_date']
        read_only_fields = ['created_by', 'created_date', 'last_modified_date']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'body', 'created_by', 'created_date', 'last_modified_date']
        read_only_fields = ['id', 'post', 'created_by', 'created_date', 'last_modified_date']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_by = UserSerializer(required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_by', 'created_date', 'last_modified_date', 'comments']
        read_only_fields = ['created_by', 'created_date', 'last_modified_date', 'comments']
