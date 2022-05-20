"""
post_reaction views handles http requests for post_reactions resource

"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rareapi.models.reaction import Reaction

from rareapi.views.reactions import ReactionSerializer
from rareapi.views.posts import PostSerializer
from rareapi.models.postReaction import PostReaction
from rareapi.models.rareUser import RareUser
from rareapi.models.post import Post

class PostReactionView(ViewSet):
    def retrieve(self, request, pk):
        try:
            # player = request.query_params.get('player', None)
            # if player is not None:
            #     post_reactions = post_reactions.filter(player_id=player)
            post_reaction = PostReaction.objects.get(pk=pk)
            serializer = PostReactionSerializer(post_reaction)
            return Response(serializer.data)
        except post_reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        post_reactions = PostReaction.objects.all()
        post = request.query_params.get('post', None)
        if post is not None:
            post_reactions = post_reactions.filter(post_id=post)
        serializer = PostReactionSerializer(post_reactions, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post_reaction instance
        """
        rare_user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk = request.data['post_id'])
        reaction = Reaction.objects.get(id=request.data['reaction_id'])
        serializer = CreatePostReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rare_user=rare_user, post=post, reaction=reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self,request, pk):
        """doc string"""
        rare_user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk = request.data['post_id'])
        reaction = Reaction.objects.get(id=request.data['reaction_id'])
        post_reaction = PostReaction.objects.get(pk=pk)
        serializer = CreatePostReactionSerializer(post_reaction, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rare_user=rare_user, post=post, reaction=reaction)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post_reaction = PostReaction.objects.get(pk=pk)
        post_reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = RareUser
        fields = ('id', 'user')
        depth =1

class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    post = PostSerializer()
    rare_user = RareUserSerializer()
    reaction = ReactionSerializer()
    class Meta:
        model = PostReaction
        fields = ('id', "post", "rare_user", "reaction")
        depth = 2

class CreatePostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('id',)