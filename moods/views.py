from django.shortcuts import render
from .serializers import UserRegesterSerializer , MoodsSerializer
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now 
from rest_framework.generics import get_object_or_404
from django.utils.dateparse import parse_date

from .models import Mood

# Create your views here.


@api_view(['POST'])
def register_user(request) : 
    serializer = UserRegesterSerializer(data=request.data)
    if serializer.is_valid() : 
        serializer.save() 
        return Response (serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def create_mood(request) :
    today = now().date()
    if Mood.objects.filter(user = request.user , date = today).exists() : 
        return Response ({"detail" : "you already recorded your mode"} , status=status.HTTP_400_BAD_REQUEST)
    

    serializer = MoodsSerializer(data =  request.data )

    if serializer.is_valid() : 
        serializer.save(user=request.user)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET' , 'PATCH']) 
@permission_classes([IsAuthenticated])
def mood_today(request): 
    today = now().date()

    mood_obj = Mood.objects.filter(user=request.user , date=today).first()

    if not mood_obj : 
        return Response ({"detail":"no mood recorded today"} , status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET' : 
        serializer = MoodsSerializer(mood_obj)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    if request.method == 'PATCH' : 
        serializer = MoodsSerializer(mood_obj , data = request.data )

        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

        
    

    


class MoodTodayView(generics.RetrieveUpdateAPIView) : 
    serializer_class = MoodsSerializer
    permission_classes=[IsAuthenticated]


    def get_object(self):
        today = now().date()
        return get_object_or_404(Mood, user=self.request.user , date=today)





@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def mood_by_date(request) : 

    date = request.query_params.get('date')

    if not date : 
        return Response({"detail" : "date param is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    date_form = parse_date(date)

    if not date_form : 
        return Response({"detaail" : "invalide date format YYY-MM-DD"} , status=status.HTTP_400_BAD_REQUEST)
    

    mood = Mood.objects.filter(user=request.user , date = date_form).first()

    if not mood : 
        return Response ({"detail" : "no mood recorded on this date"} , status=status.HTTP_404_NOT_FOUND)
    
    serializer = MoodsSerializer(mood)
    return Response(serializer.data , status=status.HTTP_200_OK)


