from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.core.exceptions import ObjectDoesNotExist

def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

def signout(request):
    logout(request)
    return render(request, 'signout.html')

@login_required
def profile(request):
    user_profile = request.user
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/templates/registration/login.html')

@login_required
def profile_update(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if profile:
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        else:
            p_form = ProfileUpdateForm(request.POST, request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()

            if profile:
                p_form.save()
            else:
                new_profile = p_form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

        if profile:
            p_form = ProfileUpdateForm(instance=profile)
        else:
            p_form = ProfileUpdateForm()

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile_update.html', context)

def default_profile_image():
    return 'media/default.png'
