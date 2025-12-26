
from django.urls import path
from .views import register_user
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView


urlpatterns = [ 
    path('register/' , register_user) ,
    path('token/' , TokenObtainPairView.as_view() ) ,
    path ('token/refresh/' ,TokenRefreshView.as_view() )

]