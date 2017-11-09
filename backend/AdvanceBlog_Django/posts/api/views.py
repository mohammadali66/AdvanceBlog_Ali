from rest_framework.generics import ListAPIView

from posts.models import Post
from . import serializers


class PostListAPIView(ListAPIView):
    
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()