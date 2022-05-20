"""
subscription views handles http requests for subscriptions resource

"""

from datetime import datetime
from django.forms import NullBooleanField
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


from rareapi.models.subscription import Subscription
from rareapi.models.rareUser import RareUser
from rareapi.models.post import Post

class SubscriptionView(ViewSet):
    def retrieve(self, request, pk):
        try:
            # player = request.query_params.get('player', None)
            # if player is not None:
            #     subscriptions = subscriptions.filter(player_id=player)
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except subscription.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    def list(self, request):
        
        subscriptions = Subscription.objects.all()
        author = request.query_params.get('author', None)
        follower = request.query_params.get('follower', None)
        if author is not None:
            subscriptions = subscriptions.filter(author_id=author)
        if follower is not None:
            subscriptions = subscriptions.filter(follower_id=follower, ended_on = None)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized subscription instance
        """
        follower = RareUser.objects.get(user=request.auth.user)
        author = RareUser.objects.get(pk = request.data['author_id'])
        serializer = CreateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, follower=follower)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self,request, pk):
        """doc string"""
        # ended-on in update
        subscription = Subscription.objects.get(pk=pk)
        ended_on = datetime.now()
        serializer = CreateSubscriptionSerializer(subscription, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(ended_on=ended_on)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
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
class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    author = RareUserSerializer()
    follower = RareUserSerializer()
    posts = PostSerializer(many=True)

    class Meta:
        model = Subscription
        fields = ('id', "author", "follower", "created_on", "ended_on", "posts")
        depth = 2

class CreateSubscriptionSerializer(serializers.ModelSerializer):
    # author = RareUserSerializer()
    # follower = RareUserSerializer()
    class Meta:
        
        model = Subscription
        fields = ['id']