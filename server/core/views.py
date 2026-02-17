from django.shortcuts import render
import json 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth import get_user_model


# Create your views here.

User = get_user_model()


def signup(request):
    """
    Registers a new user in the system 
    Method: POST 
    Request Body:
        username (str): Required, unique identifier 
        email (str): Required feild and Valid email address 

    """

