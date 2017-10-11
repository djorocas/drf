from rest_framework.serializers import ModelSerializer
from ..models import Post


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'publish', 'user']


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'publish']


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'publish']
