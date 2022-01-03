from rest_framework import viewsets, status, request
from rest_framework.decorators import action
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(methods=['POST'], detail=True)
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            meal = Meal.objects.get(id=pk)
            username = request.data['username']
            stars = request.data['stars']
            user = User.objects.get(username= username)
            try:
                #update
                rating= Rating.objects.get(user=user.id, meal=meal.id) # spécifique rate
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Updated',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
            except:
                # create if the rate not exist 
                rating = Rating.objects.create(stars=stars, meal=meal, user=user)
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Created',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_200_OK)
        else:
            json= {
                'message': 'start not provided'
            }
            return Response(json, status=status.status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer