from django.db.models import Q
from rest_framework.generics import (ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView)
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.filters import (SearchFilter, OrderingFilter)

from .permissions import IsOwnerOrReadOnly
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
from ..models import Post


# ListAPIView: returns a queryset
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "content"]

    def get_queryset(self, *args, **kwargs):
        queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)).distinct()
        return queryset_list


# RetrieveAPIView: only retrieves one Instance
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
