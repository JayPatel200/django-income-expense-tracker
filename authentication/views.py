from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth

# Validates the email by checking format
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, email is already in use, please choose another one.'}, status=409)
        return JsonResponse({'email_valid': True})
    
# Validates the username
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, username is already in use, please choose another one.'}, status=409)
        return JsonResponse({'username_valid': True})
        
# Registers a new user
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # GET USER DATA
        username = request.POST['username'];
        email = request.POST['email'];
        password = request.POST['password'];
        context = {
            'fieldValues': request.POST
        }
        # VALIDATE 
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, 'Password should altleast be 6 characters long')
                    return render(request, 'authentication/register.html', context)
                                
                # CREATE A USER ACCOUNT
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'success')
                return redirect('login')

        return render(request, 'authentication/register.html')

# Logins an existing user by confirming their credentials  
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, 'Welcome '+ user.username + ' you are now logged in!')
                return redirect('expenses')
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Please fill all the fields')
        return render(request, 'authentication/login.html')

# Logs out a user   
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect('login')