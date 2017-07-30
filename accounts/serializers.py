from rest_framework import serializers
from rest_framework.response import Response

from accounts.models import User
from blog.models import Article

from blog.serializers import ArticleSerializer


class UserSerializer(serializers.ModelSerializer):
    likes_number = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()

    def get_articles(self, obj):
        return ArticleSerializer(Article.objects.filter(
            liked_by__in=[obj]), many=True).data

    def get_likes_number(self, obj):
        return Article.objects.filter(liked_by__in=[obj]).count()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'photo',
            'birthday',
            'likes_number',
            'articles'
        )


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, attrs):
        user = self.context.get('user')

        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError('incorrect password!!!!')

        if attrs.get('new_password') != attrs.get('new_password2'):
            raise serializers.ValidationError('not equal passwords!!!!')

        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Class based on User model and 
    describes the interface for user login request.
    """
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        # check email
        if not self.Meta.model.objects.filter(
                email__iexact=attrs.get('email')):
            raise serializers.ValidationError(
                'The username exists. Please try another one.')
        # check password
        else:
            data = self.Meta.model.objects.get(
                email=attrs.get('email'))
            if not data.check_password(attrs.get('password')):
                raise serializers.ValidationError(
                    'The password wrong. Please try another one.')
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Class based on User model and describes
    the interface for user registration request with next fields:
    username, email, password1, password2.
    """
    password2 = serializers.CharField(min_length=6, max_length=40)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        # check username
        if self.Meta.model.objects.filter(
                username__iexact=attrs.get('username')).exists():
            raise serializers.ValidationError(
                'The username already exists. Please try another one.')
        # check email
        elif self.Meta.model.objects.filter(
                email__iexact=attrs.get('email')).exists():
            raise serializers.ValidationError(
                'The email already exists. Please try another one.')
        # check password
        elif attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError('Passwords don\'t match.')

        return attrs


class UserForgetPasswordSerializer(serializers.Serializer):
    """
    Class based on Serializer model and describes the 
    interface for user request with next recovery password
    and sending it to user email.
    """
    email_or_username = serializers.CharField(min_length=5, max_length=255)

    def validate(self, attrs):
        # check username or email
        check_point = attrs.get('email_or_username')
        if '@' in check_point:
            if not User.objects.filter(email__iexact=check_point).exists():
                raise serializers.ValidationError(
                    'The email not exist. Please try another one.')
        else:
            if not User.objects.filter(username__iexact=check_point).exists():
                raise serializers.ValidationError(
                    'The username not exist. Please try another one.')
        return attrs


class UserShortInfoSerializer(serializers.ModelSerializer):
    """
    Class based on User model and describes 
    the interface with short information about user:
    id, username, email, date_joined.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']


class MyUserChangePasswordSerializer(serializers.Serializer):
    """
    Class based on Serializer model and describes 
    the interface for user change password, with next fields:
    old_password - take old password and check if it correct,
    new_password1 and mew_password2 - take new password, 
    check if it the same and use it for creating new password.
    """

    old_password = serializers.CharField(min_length=6, max_length=40)
    new_password1 = serializers.CharField(min_length=6, max_length=40)
    new_password2 = serializers.CharField(min_length=6, max_length=40)

    def validate(self, attrs):
        user = self.context.get('user')
        # check if user input correct old password
        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError(
                'The password wrong. Please try another one.')
        # check if user input the same new password twice
        if attrs.get('new_password1') != attrs.get('new_password2'):
            raise serializers.ValidationError('Passwords don\'t match.')
        # check if user don't use old password like new password
        if attrs.get('old_password') == attrs.get('new_password1'):
            raise serializers.ValidationError(
                'You can\'t use old password like new password')

        return attrs


class UserMainInfoSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password')
