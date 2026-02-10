from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from django.db import IntegrityError

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    """
    Handle user registration.
    Expects JSON: { "username": "string", "email": "string", "password": "string" }
    Returns 201 on success, 400 on validation error, 409 if user exists
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"},
            status=400
        )

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Validation
    if not username or not email or not password:
        return JsonResponse(
            {"error": "Username, email, and password are required"},
            status=400
        )

    if len(password) < 8:
        return JsonResponse(
            {"error": "Password must be at least 8 characters long"},
            status=400
        )

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"error": "Username already exists"},
            status=409
        )

    if User.objects.filter(email=email).exists():
        return JsonResponse(
            {"error": "Email already exists"},
            status=409
        )

    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "User created successfully"
            },
            status=201
        )
    except IntegrityError:
        return JsonResponse(
            {"error": "Error creating user"},
            status=400
        )


@csrf_exempt
@require_http_methods(["POST"])
def signin(request):
    """
    Handle user login.
    Expects JSON: { "username": "string", "password": "string" }
    Returns 200 on success, 401 on invalid credentials, 400 on validation error
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"},
            status=400
        )

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    # Validation
    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required"},
            status=400
        )

    # Authenticate user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Login user (creates session)
        login(request, user)
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "Login successful"
            },
            status=200
        )
    else:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=401
        )


@csrf_exempt
@require_http_methods(["POST"])
def signout(request):
    """
    Handle user logout.
    Returns 200 on success
    """
    logout(request)
    return JsonResponse(
        {"message": "Logout successful"},
        status=200
    )
