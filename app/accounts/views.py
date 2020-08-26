from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView as logout_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.utils.translation import ugettext as _

from .forms import ProfileForm, RegisterForm, LoginForm, SettingsForm
from .models import UserProfile

import os



context_base = {}



def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:profile'))

    context = context_base

    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = LoginForm(request.POST)

        if form.is_valid():

            # get the user by email or username
            username = User.objects.get(
                Q(username=form.cleaned_data['username_email']) |
                Q(email=form.cleaned_data['username_email'])
            ).username

            # pass the username and password to authenticate() to login
            user = authenticate(
                username = username,
                password = form.cleaned_data['password'],
            )
            if user is not None:
                # authentication successful
                login(request, user)

                # redirect to next url
                return HttpResponseRedirect(form.cleaned_data['next'])
            else:
                # authentication failed, add error to form
                form.add_error(None, ValidationError(
                    _('Invalid Password.'),
                ))

    else:
        form = LoginForm()

    context['form'] = form

    # next url after login is stored in GET param. default to profile
    context['next'] = request.GET.get('next', reverse('accounts:profile'))

    return render(request, 'accounts/login.html', context)



def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:profile'))
    if os.environ.get("REGISTRATION")==None or bool(os.environ.get("REGISTRATION"))==True:
        if request.method == 'POST':

            # create a form instance and populate it with data from the request
            form = RegisterForm(request.POST)

            if form.is_valid():

                # create a new user
                new_user = User.objects.create_user(username=form.cleaned_data['username'])
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()

                # login after creation
                new_user = authenticate(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'],
                )
                login(request, new_user)

                # redirect
                return HttpResponseRedirect(reverse('accounts:profile'))

        else:
            form = RegisterForm()

        return render(request, 'accounts/register.html', {'form': form})
    else: 
        return HttpResponseRedirect('/')


@login_required
def profile(request):

    user = request.user
    message = ""

    current_info = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    current_settings = {
        'darkmode': user.profile.darkmode
    }
    settings_form = SettingsForm(current_settings)
    # return HttpResponse("this is the user profile page for username '%s'. update first, last, email, username, and password here." % request.user.username)
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = ProfileForm(request.POST)
        

        if form.is_valid():

            if form.cleaned_data['username'] != user.username:
                user.username = form.cleaned_data['username']

            if form.cleaned_data['first_name'] != user.first_name:
                user.first_name = form.cleaned_data['first_name']

            if form.cleaned_data['last_name'] != user.last_name:
                user.last_name = form.cleaned_data['last_name']

            if form.cleaned_data['email'] != user.email:
                user.email = form.cleaned_data['email']

            if form.cleaned_data['password'] != user.password and form.cleaned_data['password'] != "":
                user.set_password(form.cleaned_data['password'])

            user.save()
            message += "Profile updated."

            return render(request, 'accounts/profile.html', {'form': form, 'settings_form': settings_form, 'message': message})

    else:
        form = ProfileForm(current_info)

    return render(request, 'accounts/profile.html', {'form': form, 'settings_form': settings_form})

@login_required
def settings(request):

    user = request.user
    message = ""

    current_info = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    current_settings = {
        'darkmode': user.profile.darkmode
    }

    

    form = ProfileForm(current_info)

    # return HttpResponse("this is the user profile page for username '%s'. update first, last, email, username, and password here." % request.user.username)
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        settings_form = SettingsForm(request.POST)

        if settings_form.is_valid():

            if settings_form.cleaned_data['darkmode'] != user.profile.darkmode :
                user.profile.darkmode = settings_form.cleaned_data['darkmode']

            user.profile.save()
            message += "Profile updated."

            

            return render(request, 'accounts/profile.html', {'form': form, 'settings_form': settings_form, 'message': message})

    else:
        settings_form = SettingsForm(current_settings)

    return render(request, 'accounts/profile.html', {'form': form, 'settings_form': settings_form})
