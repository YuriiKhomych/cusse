from rest_framework import serializers

from blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title')


class ArticleFullDataSerializer(serializers.ModelSerializer):
    """
    Class based on Article model and describes the 
    interface with full information about article:
    title, body, data, author, liked_by.
    """

    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'liked_by']


class ArticleCreateSerializer(serializers.ModelSerializer):
    """
    Class based on Article model and describes the 
    interface for creating new article.
    User can write only article title and body, 
    author and data will add automaticaly.
    """
    class Meta:
        model = Article
        fields = ['title', 'body']

    def validate(self, attrs):
        # check the title name for uniqueness
        if Article.objects.filter(title__exact=attrs.get('title')).exists():
            raise serializers.ValidationError(
                'Sorry, article with this title already exist. Please rename your article title'
            )
        return attrs


class ArticleRemoveSerializer(serializers.ModelSerializer):
    """
    Class based on Article model and describes the interface for removing 
    article by title,
    I suppose user know only this article parameter and don't see article id.
    """
    title = serializers.CharField()

    class Meta:
        model = Article
        fields = ['title']

    def validate(self, attrs):
        # check if the title is exist
        if not Article.objects.filter(title__exact=attrs.get('title')).exists():
            raise serializers.ValidationError(
                'Sorry, but article with title {} not exist'.format(
                    attrs.get('title')))
        return attrs


class ArticleSearchSerializer(serializers.Serializer):
    """
    Class based on Serializer model and describes the interface for searching 
    article by some words or
    letters in article title or body.
    """
    search_keyword = serializers.CharField()
