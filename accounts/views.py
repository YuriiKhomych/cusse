from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import LoginForm, SignUpForm


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('all_articles'))
    else:
        form = LoginForm
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(email=data.get('email'), password=data.get('password'))
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse('all_articles'))
                else:
                    print('sorry')
        return render(request, 'sign-in.html', {'form': form})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('sign_in'))


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            user = authenticate(email=data.get('email'),
                                password=data.get('password1'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('all_articles'))
            else:
                print('sorry')
    else:
        form = SignUpForm()
    return render(request, 'sign-up.html', {'form': form})