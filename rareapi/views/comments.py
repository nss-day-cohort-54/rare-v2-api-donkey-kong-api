"""
comment views handles http requests for comments resource

"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


from rareapi.models.comment import Comment
from rareapi.models.rareUser import RareUser
from rareapi.models.post import Post

class CommentView(ViewSet):
    def retrieve(self, request, pk):
        try:
            # player = request.query_params.get('player', None)
            # if player is not None:
            #     comments = comments.filter(player_id=player)
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    def list(self, request):
        comments = Comment.objects.all()
        post = request.query_params.get('post', None)
        if post is not None:
            comments = comments.filter(post_id=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized comment instance
        """
        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk = request.data['post'])
        serializer = CreatecommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self,request, pk):
        """doc string"""
        
        comment = Comment.objects.get(pk=pk)
        serializer = CreatecommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = RareUser
        fields = ('id', 'user')
        depth =1
class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    author = RareUserSerializer()
    class Meta:
        model = Comment
        fields = ('id', "content", "post", "author", "created_on")
        depth = 2

class CreatecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', "content", "post", "author"]