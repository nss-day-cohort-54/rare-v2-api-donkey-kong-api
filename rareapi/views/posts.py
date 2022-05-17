from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models.category import Category
from rareapi.models.post import Post
from rareapi.models.rareUser import RareUser
from rareapi.views.rare_user import RareUserSerializer


class PostView(ViewSet):
    """_summary_

    Args:
        ViewSet (_type_): _description_
    """

    def retrieve(self, request, pk):
        """_summary_"""
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """_summary_"""
        rare_user = RareUser.objects.get(user=request.auth.user)
        serialized_user = RareUserSerializer(rare_user)
        if serialized_user.data["user"]["is_staff"]:
            posts = Post.objects.all()
        else:
            posts = Post.objects.all().filter(approved=1)
            publication_date = Post.objects.get(
                publication_date=request.data['publication_date'])
            posts = posts.filter(publication_date <= datetime.now())
        posts = posts.order_by('-publication_date')
        category = request.query_params.get('label', None)
        if category is not None:
            posts = posts.filter(category=category)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """_summary_"""
        post = Post.objects.get(pk=pk)
        serializer = CreatePostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # post.categories.remove(*post.categories.all())
        # post.categories.add(*request.data['categories'])

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """Handle POST operations Returns:
            Response -- JSON serialized game instance
        """
        # Any foreign keys needed must be stored in a variable
        # like this

        rare_user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data['category'])
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rare_user=rare_user, category=category)
        # post = Post.objects.get(pk=serializer.data['id'])
        # post.categories.add(*request.data['category'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """_summary_"""
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


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
            'approved',
            'tags'
        )
        depth = 2


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # uses an array because information is coming from
        # front-end
        fields = (
            'id',
            'title',
            'publication_date',
            'image_url',
            'content',
            'approved',
            'category',
            'rare_user',
            'tags'
        )
        depth = 2
