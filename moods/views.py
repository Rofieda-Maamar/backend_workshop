from django.shortcuts import render
from .serializers import UserRegesterSerializer , MoodsSerializer
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now 
from rest_framework.generics import get_object_or_404
from django.utils.dateparse import parse_date
from django.db.models import Count

from .models import Mood
from datetime import datetime

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




### 


@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def mood_hostory(request) : 
    moods= Mood.objects.filter(user=request.user).order_by('-date')
    serializer = MoodsSerializer(moods , many = True)
    return Response ( serializer.data , status=status.HTTP_200_OK)



import calendar

@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def yearly_month_stats(request) :
    moods= Mood.objects.filter(user=request.user)
    current_year = datetime.now().year-1
    all_moods = ['happy' , 'sad' , 'angry']

    monthly_result={}

    for month in range(1,13) : 
        moods_in_month = moods.filter(date__year=current_year , date__month= month )
        stats = moods_in_month.values('mood').annotate(count =Count('mood'))
        stat_dict = {item['mood'] : item['count'] for item in stats }
        
        month_name = calendar.month_name[month]

        month_counts = {} 

        for mood in all_moods : 
            month_counts[mood]  = stat_dict.get(mood , 0)

        monthly_result[month_name] = month_counts


    return Response(monthly_result , status=status.HTTP_200_OK)


  