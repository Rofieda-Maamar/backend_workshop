
from django.urls import path
from .views import register_user , create_mood , mood_today , MoodTodayView , mood_by_date
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView


urlpatterns = [ 
    path('register/' , register_user) ,
    path('mood/' , create_mood) ,
    path('mood/update/' , mood_today) ,
    path('mood/search/' , mood_by_date) ,
    path('mood/view/' , MoodTodayView.as_view()) ,
    path('token/' , TokenObtainPairView.as_view() ) ,
    path ('token/refresh/' ,TokenRefreshView.as_view() )

]