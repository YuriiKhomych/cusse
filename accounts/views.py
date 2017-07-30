from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.core.mail import send_mail

from utils import random_word
from utils import gen_page_list

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from accounts.forms import LoginForm, SignUpForm
from accounts.models import User

from accounts.serializers import UserLoginSerializer, UserSerializer,\
    UserCreationSerializer, UserChangePasswordSerializer, \
    UserMainInfoSerializer, UserRegistrationSerializer, \
    MyUserChangePasswordSerializer, UserForgetPasswordSerializer, \
    UserShortInfoSerializer

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
                user = authenticate(
                    email=data.get('email'),
                    password=data.get('password')
                )
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


@api_view(['POST'])
def get_user_django(request):
    user = User.objects.get(pk=1)
    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username
    }
    return JsonResponse(user_info)


@api_view(['GET', 'POST'])
def get_user_rest(request):
    if request.method == 'GET':
        # serializer for return formatted data
        user = User.objects.get(pk=1)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'POST':
        # serializer for validation request
        serializer = UserCreationSerializer(data=request.POST)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            print(validated_data)
            return Response({'success': True})
        else:
            return Response(serializer.errors)


@api_view(['POST'])
def change_user_password(request):
    user = User.objects.get(pk=2)
    serializer = UserChangePasswordSerializer(
        data=request.POST,
        context={'user': user}
    )
    if serializer.is_valid():
        validated_data = serializer.validated_data
        user.set_password(validated_data.get('new_password'))
        user.save()
        return Response({'success': True})
    else:
        return Response(serializer.errors)


class UserLoginAPI(APIView):
    """
    This view will check input user email and password then,
     if data is valid, login him in system
    end send back response with user basic information:
     username, email, first_name, date_joined.
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if request.user.is_authenticated():
            return Response({'Sorry, you are already login'},
                            status=status.HTTP_409_CONFLICT)

        else:
            if serializer.is_valid():
                validate_data = serializer.validated_data
                # authenticate user
                user = authenticate(email=validate_data.get('email'),
                                    password=validate_data.get('password'))
                if user:
                    # collect information about user
                    user_data = User.objects.get(
                        email__iexact=validate_data.get('email'))
                    context = {
                        'username': user_data.username,
                        'email': user_data.email,
                        'first_name': user_data.first_name,
                        'date_joined': user_data.date_joined,
                        }
                    return Response(context)
                else:
                    return 'User does not exist'
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )


class UserRegistrationAPI(APIView):
    """
    This view will check input user name, email,
    password then, if data is valid, create new user, login him in system
    and send back response with user Token.
    """
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # Add permission class in future
        if request.user.is_authenticated():
            return Response({'Sorry, you are registered'},
                            status=status.HTTP_409_CONFLICT)
        else:
            if serializer.is_valid():
                validate_data = serializer.validated_data
                # create user
                user = User.objects.create_user(
                    username=validate_data.get('username'),
                    email=validate_data.get('email'),
                )
                user.set_password(validate_data.get('password'))
                user.save()
                # login user
                login(request, authenticate(
                    email=validate_data.get('email'),
                    password=validate_data.get('password')))
                # create token
                token = Token.objects.create(user=user)
                return JsonResponse(token.key)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UserForgetPasswordAPI(APIView):
    """
    This view will check input user name or email,
    then generate new password and sent it to user email.
    """
    serializer_class = UserForgetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            # find user object
            if '@' in validate_data.get('email_or_username'):
                user = User.objects.get(
                    email=validate_data.get('email_or_username'))
            else:
                user = User.objects.get(
                    username=validate_data.get('email_or_username'))
            # generate and password
            password = random_word(10)
            user.set_password(password)
            user.save()
            # send mail
            send_mail('Your new password',
                      'Hi, it\'s you new password: {}'.format(password),
                      'yuriykhomich@gmail.com',
                      [user.email]
                      )
            return Response({'success': True})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserShortInfoAPI(ListAPIView):
    """
    This view will return response with
    short information(id, username, email, date_joined) about all users,
    and divided into 10 users objects at the one page.
    """
    queryset = User.objects.all()
    serializer_class = UserShortInfoSerializer
    pagination_class = PageNumberPagination


class UserChangePasswordAPI(APIView):
    """
    This view will check input user old password and new password,
     then, if data is valid, update user password at base.
    """
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'user': request.user})

        if serializer.is_valid():
            validate_data = serializer.validated_data
            # create new user password and save it in base
            request.user.set_password(validate_data.get('new_password1'))
            request.user.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ChangeUserPasswordView(APIView):
    serializer_class = MyUserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'user': request.user})
        if serializer.is_valid():
            validated_data = serializer.validated_data
            request.user.set_password(validated_data.get('new_password'))
            request.user.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MainUserFieldsView(APIView):
    serializer_class = UserMainInfoSerializer

    def post(self, request):
        username = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                user_info = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username
                }
                return Response(user_info)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UsersView(GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            user = self.get_object()
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)



class UserCreateView(APIView):
    model = User
    serializer_class = UserCreationSerializer
    # token = Token.objects.create(user=User.objects.get(pk=3))
    # queryset = User.objects.all()
    # serializer_class = UserCreationSerializer
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     token, created = Token.objects.get_or_create(user=serializer.instance)
    #     return Response({'token': token.key, 'id': serializer.instance.id},
    #                     status=status.HTTP_201_CREATED, headers=headers)
