# ATTENTION!!! THIS IS COPIED AND PASTED FROM GAMER-RATER
# NEEDS REFACTORING
"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rareapi.models.category import Category


class CategoryView(ViewSet):
    """Level up category types view"""

    def retrieve(self, request, pk):
        """The retrieve method will get a single object 
        from the database based on the pk (primary key) in 
        the url. We will use the ORM to get the data, then the 
        serializer to convert the data to json. Add the 
        following code to the retrievemethod, making sure 
        the code is tabbed correctly:

        Returns:
            Response -- JSON serialized category type
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """The list method is responsible for getting 
        the whole collection of objects from the database. 
        The ORM method for this one is all. Here is the code 
        to add to the method:

        Returns:
            Response -- JSON serialized list of category types
        """
        categories = Category.objects.all()
        # Add in the next 3 lines
        # gamer = request.query_params.get('id', None)
        # if gamer is not None:
        #     games = games.filter(gamer_id=gamer)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        category = Category.objects.get(pk=pk)
        serializer = CreateCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """
        # category = Category.objects.get(pk=request.data['category'])
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    The serializer class determines how the Python data should
    be serialized to be sent back to the client. Put the
    following code at the bottom of the same module as above.
    Make sure it is outside of the view class.
    """
    class Meta:
        model = Category
        fields = (
            'id',
            'label'
        )
        depth = 1


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # uses an array because information is coming from
        # front-end
        fields = (
            'id',
            'label'
        )
        depth = 1
