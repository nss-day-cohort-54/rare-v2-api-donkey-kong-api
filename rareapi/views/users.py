from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models.rareUser import RareUser

class UserView(ViewSet):
    
    def retrieve(self, request, pk):

        try:
            rare_user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rare_user)
            return Response(serializer.data)
        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):

        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)
class UserSerializer(serializers.Serializer):
    fields = ("username", "first_name", "last_name", "is_staff")
class RareUserSerializer(serializers.Serializer):
    user = UserSerializer
    fields = ("id","user","active")
