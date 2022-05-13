from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models import rareUser
from rareapi.models.post import Post

from rareapi.models.post import Post
from rareapi.models.rareUser import RareUser


class PostView(ViewSet):

    def retrieve(self, request, pk):

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):

        posts = Post.objects.all()
        rare_user = RareUser.objects.get(user=request.auth.user)
        category = request.query_params.get('label', None)
        if category is not None:
            posts = posts.filter(category=category).filter(user=rare_user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    The serializer class determines how the Python data should
    be serialized to be sent back to the client. Put the
    following code at the bottom of the same module as above.
    Make sure it is outside of the view class.
    """
    class Meta:
        model = Post
        fields = (
            'id',
            'rare_user',
            'category',
            'title',
            'publication_date',
            'image_url',
            'content',
            'approved'
        )
        depth = 2
