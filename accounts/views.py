from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
from .forms import *
from django.contrib import messages


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated in successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'section': 'login'})   

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'accounts/register_done.html', {'user_form': user_form, 'new_user': new_user,'section':'register'})
    else:
        user_form = UserRegistrationForm()
    return render(request,'accounts/template/register.html', {'user_form': user_form, 'section':'register'})


@login_required
@transaction.atomic
def edit(request):
    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Handle user form
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        # Check if forms are valid and save them
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        # If not, return forms
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            messages.error(request, 'Error updating profile')
        return redirect('dashboard')
        # render to edit.html
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html', {'user_form': user_form, 'profile_form': profile_form,'section': 'edit_profile'})
