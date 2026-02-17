from django.shortcuts import render
import json 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q # Q is for Or queries 

# Create your views here.

User = get_user_model()

@csrf_exempt
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
            "username": xyz
            "email": "f2024xxxx@goa.bits-pilani.ac.in",
            "created_at": time the user is created at 
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
                    'email': user.email, 
                    'created_at': user.date_joined.isoformat() 
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
        

@csrf_exempt
def signin(request):
    """
    Autheticate the user and establish the session 
    Method: POST
    Request:
        - identity (str): Can be the username OR the email.
        - password (str): Required.
    Returns:
        - 200 OK: { 
            "message":  
            "username": 
            "email": 
            "role":  
            "joined_at": 
        }
        - 401 Unauthorized: Invalid credentials.
        - 400 Bad Request: Missing fields.

    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            identity = data.get('identity', '').strip()
            password = data.get('password')

            # validation for missing feilds 
            if not identity or not password:
                return JsonResponse(
                    {'error': 'Identity and password are required.'},
                    status=400  # bad request: missing feild 
                )
            
            # lookup the user by email or username 
            user_obj = User.objects.filter(
                Q(username=identity) | Q(email=identity)
            ).first()

            if user_obj:
                # Authenticate using the actual username found and the password 
                # verfying the password of the user 
                user = authenticate(request, username=user_obj.username, password=password)

                if user is not None:
                    # the user details are correct so establish the session
                    login(request, user)

                    return JsonResponse({
                            'message': 'Login Successful!',
                            'username': user.username,
                            'email': user.email,
                            'role': user.role,
                            'joined_at': user.date_joined.isoformat()
                        }, status=200
                    )
                
            # same error for both "user not found" and "wrong password"
            return JsonResponse(
                {'error': 'Invalid credentials.'}, 
                status=401
            )
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server Error: {str(e)}'}, status=500)
            # some internal server error 
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
        # method must be POST



@csrf_exempt
def signout(request):
    """
    Logs out the user and clears the session.
    Method: POST
    Returns:
        - 200 OK: { "message": "Logged out successfully." }
        - 405 Method Not Allowed: If request is not POST.
    """
    if request.method == 'POST':
        # logout(): it deletes the session from the DB and tells the browser to clear the session cookie.
        logout(request)
        
        return JsonResponse(
            {'message': 'Logged out successfully.'}, 
            status=200
        )
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)