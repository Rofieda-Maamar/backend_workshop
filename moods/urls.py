
from django.urls import path
from .views import register_user , create_mood , mood_today , MoodTodayView , mood_by_date , mood_hostory , yearly_month_stats
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView


urlpatterns = [ 
    path('register/' , register_user) ,
    path('mood/' , create_mood) ,
    path('mood/update/' , mood_today) ,
    path('mood/search/' , mood_by_date) ,
    path('mood/history/' , mood_hostory) ,
    path('mood/stats/' , yearly_month_stats) ,
    path('mood/view/' , MoodTodayView.as_view()) ,
    path('token/' , TokenObtainPairView.as_view() ) ,
    path ('token/refresh/' ,TokenRefreshView.as_view() )

]