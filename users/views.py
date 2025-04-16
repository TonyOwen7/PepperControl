from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib import messages

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to the homepage or any other page

def login_view(request):
    # Initialize the login attempts counter in the session
    if 'login_attempts' not in request.session:
        request.session['login_attempts'] = 0

    # Maximum number of login attempts allowed
    MAX_ATTEMPTS = 3

    if request.method == 'POST':
        MAX_ATTEMPTS = 3
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Reset login attempts on successful login
                request.session['login_attempts'] = 0
                return redirect('/robots/')  # Redirect to home page after login
            else:
                # Increment login attempts on failed login
                request.session['login_attempts'] += 1
                attempts_left = MAX_ATTEMPTS - request.session['login_attempts']
                messages.error(request, f'Invalid username or password. Attempts left: {attempts_left}')
        else:
            # Increment login attempts on invalid form submission
            request.session['login_attempts'] += 1
            attempts_left = MAX_ATTEMPTS - request.session['login_attempts']
            messages.error(request, f'Invalid form submission. Attempts left: {attempts_left}')

        # Check if login attempts exceed the limit
        if request.session.get('login_attempts', 0) >= MAX_ATTEMPTS:
            messages.error(request, 'You have exceeded the maximum number of login attempts. Please try again later.')
            # Reset login attempts and redirect to home page
            request.session['login_attempts'] = 0
            return redirect('/')  # Redirect to home page
    else:
        form = LoginForm()

    # Pass the number of attempts left to the template
    attempts_left = MAX_ATTEMPTS - request.session.get('login_attempts', 0)
    return render(request, 'users/login.html', {'form': form, 'attempts_left': attempts_left})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('robot_configuration')  # Redirect to home page after registration
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
