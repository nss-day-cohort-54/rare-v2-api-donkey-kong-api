from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models.rareUser import RareUser


class RareUserView(ViewSet):

    # def retrieve(self, request, pk):

    #     try:
    #         rare_user = RareUser.objects.get(pk=pk)
    #         serializer = RareUserSerializer(rare_user)
    #         return Response(serializer.data)
    #     except Post.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):

        rare_user = RareUser.objects.all()
        serializer = RareUserSerializer(rare_user, many=True)
        return Response(serializer.data)


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    The serializer class determines how the Python data should
    be serialized to be sent back to the client. Put the
    following code at the bottom of the same module as above.
    Make sure it is outside of the view class.
    """
    class Meta:
        model = RareUser
        fields = (
            'id',
            'user',
            'bio',
            'profile_image_url',
            'created_on',
            'active'
        )
        depth = 2


class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        # uses an array because information is coming from
        # front-end
        fields = (
            'id',
            'user',
            'bio',
            'profile_image_url',
            'created_on',
            'active'
        )
        depth = 2
