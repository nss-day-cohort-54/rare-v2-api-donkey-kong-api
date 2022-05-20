"""View module for handling requests about reactions"""
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action

from rareapi.models import Reaction
from rareapi.models.rareUser import RareUser
from rareapi.views.rare_user import RareUserSerializer

class ReactionView(ViewSet):
    """Level up reactions view"""

    def list(self, request):
        """Handle GET requests to get all reactions

        Returns:
            Response -- JSON serialized list of reactions
        """
        reactions = Reaction.objects.all().order_by('label')
        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """_summary_

        Args:
            request (_type_): _description_
            pk (_type_): _description_
        """
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction)
            return Response(serializer.data)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        # if statement that checks if requesting user is an admin
        rare_user = RareUser.objects.get(user=request.auth.user)
        rare_user = RareUserSerializer(rare_user)
        if rare_user.data["user"]["is_staff"]:
            # if true run below
            serializer = CreateReactionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if false return an error message
        else:
            return Response({"message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, pk):
        """_summary_

        Args:
            request (_type_): _description_
            pk (_type_): _description_

        Returns:
            _type_: _description_
        """
        reaction = Reaction.objects.get(pk=pk)
        reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        """_summary_"""
        reaction = Reaction.objects.get(pk=pk)
        serializer = CreateReactionSerializer(reaction, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # post.categories.remove(*post.categories.all())
        # post.categories.add(*request.data['categories'])

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
        depth = 1


class CreateReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
