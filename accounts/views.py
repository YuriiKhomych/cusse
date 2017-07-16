from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from accounts.forms import LoginForm, SignUpForm
from accounts.models import User

from utils import gen_page_list


def all_users(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(User.objects.all(), 10)
    try:
        page_come = paginator.page(page)
    except PageNotAnInteger:
        page_come = paginator.page(1)
    except EmptyPage:
        page_come = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {
        'users': page_come,
        'pagination': gen_page_list(page, paginator.num_pages)
    })


def single_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'single-user.html', {'user': user})


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