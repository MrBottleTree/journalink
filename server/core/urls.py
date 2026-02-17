from django.urls import path 
from . import views    

urlpatterns = [
    # the urls begin with api/ 
    path('auth/signup/', views.signup, name='signup'),
    path('auth/signin/', views.signin, name='signin')
]