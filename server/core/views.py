from django.shortcuts import render
import json 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth import get_user_model
from django.http import JsonResponse


# Create your views here.

User = get_user_model()


def signup(request):
    """
    Registers a new user in the system 
    Method: POST 
    Request Body:
        - username (str): Required, unique identifier 
        - email (str): Required feild and Valid bits email address
        - password (Str): will be hashed before storing in the database 
        - role (str): Optional => 'STUDENT' (Default) or 'PROFESSOR'

    Returns:
        - 201 Created: {
            "message": "Account created successfully!",
            "user_id": 1,
            "email": "f2024xxxx@goa.bits-pilani.ac.in",
            "username": xyz
        }
        - 405 Method Not allowed: The request must a POST method 
        - 409 Conflict: Account already exists in the database with the given credientials 
        - 403 Forbidden: Email is not a valid bits email id 
        - 400 Bad Request: missing feilds or invalid json request send by the user 
    """

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            username = data.get('username')
            email = data.get('email', ' ').strip().lower()
            password = data.get('password')
            role = data.get('role', 'STUDENT')

            # validation if the feilds are not empty (msissing feilds)
            if not username or not email or not password:
                return JsonResponse(
                    {'error': 'username, email and password are required feilds'},
                    status=400     # bad request => missing feilds 
                )
            
            # bits email verification
            ALLOWED_DOMAIN = "@goa.bits-pilani.ac.in"
            if not email.endswith(ALLOWED_DOMAIN):
                return JsonResponse(
                    {'error': f'Registration is restricted to {ALLOWED_DOMAIN} emails only.'},
                    status=403   # Forbidden => email is not valid 
                )
            
            # database check => if the account already exists or not 
            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {'error': 'That username is already taken.'}, 
                    status=409   # conflict => username is taken
                )
            
            if User.objects.filter(email=email).exists():
                return JsonResponse(
                    {'error': 'The email is already registered.'},
                    status=409   # conflict => account already exists 
                )
            
            # now create the user as all the checks are done 
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,    # django hashes the password on its own 
                role=role
            )

            # success respone as the user is created 
            return JsonResponse(
                {
                    'message': 'Account created successfully!',
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email 
                },
                status=201  # created 
            )
        
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON format.'}, 
                status=400   # bad request 
            )
        except Exception as e:
            return JsonResponse(
                {'error': f'Server Error: {str(e)}'}, 
                status=500      # internal server error 
            )
    # if the request is other than POST 
    else:
        return JsonResponse(
            {'error': 'Method not allowed.'}, 
            status=405   # method not allowed status code = 405
        )
        

