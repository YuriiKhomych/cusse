from rest_framework import serializers
from rest_framework.response import Response

from accounts.models import User
from blog.models import Article

from blog.serializers import ArticleSerializer


class UserSerializer(serializers.ModelSerializer):
    likes_number = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()

    def get_articles(self, obj):
        return ArticleSerializer(Article.objects.filter(liked_by__in=[obj]), many=True).data

    def get_likes_number(self, obj):
        return Article.objects.filter(liked_by__in=[obj]).count()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'photo', 'birthday', 'likes_number', 'articles')


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




class UserMainInfoSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password')

