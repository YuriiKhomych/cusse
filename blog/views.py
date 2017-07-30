from django.shortcuts import render, HttpResponse, HttpResponseRedirect,\
    Http404, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError
from rest_framework.permissions import AllowAny

from blog.models import Article
from blog.forms import SearchForm

from blog.serializers import (
    ArticleSerializer,
    ArticleFullDataSerializer,
    ArticleCreateSerializer,
    ArticleRemoveSerializer,
    ArticleSearchSerializer
)

from utils import gen_page_list, send_email


def blogs(request):

    form = SearchForm(request.GET)
    if form.is_valid():
        # data = form.cleaned_data
        keyword = request.GET.get('search_text', '')
        # How do it? (title__contains=data.get(keyword))
        articles = Article.objects.filter(title__contains=keyword)
    else:
        form = SearchForm()
        articles = Article.objects.all()

    # pagination part
    page = request.GET.get('page', 1)
    p = Paginator(articles, 1)
    try:
        final_articles = p.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        final_articles = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        final_articles = p.page(p.num_pages)
    return render(request,
                  'blogs.html',
                  {'articles': final_articles,
                   'form': form,
                   'pagination': gen_page_list(page, p.num_pages)})


def single_blog(request, article_id):
    # try:
    #     # select * from blog_article where id = 2
    #     article = Article.objects.get(id=article_id)
    #     return render(request, 'single-blog.html', {'article': article})
    # except Article.DoesNotExist:
    #     raise Http404
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'single-blog.html', {'article': article})


def user_articles(request, user_id):
    # 13
    user = get_object_or_404(User, id=user_id)
    # user or 404
    articles = Article.objects.filter(author=user)
    return render(request, 'user-blog.html', {'articles': articles,
                                              'user': user})


def like_article(request, article_id):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.liked_by.all():
            article.liked_by.remove(request.user)
        else:
            article.liked_by.add(request.user)
        article.save()
        return HttpResponseRedirect(reverse('all_articles'))
    else:
        return HttpResponseRedirect(reverse('sign_up'))


@api_view(['GET'])
def send_email_rest(request):
    content = {
        'first_name': 'John',
        'last_name': 'Smith'
    }
    send_email('hello',
               'shovtenko.valya@gmail.com',
               'hello-mail.html',
               content)
    return Response({'success': True})


# class ArticlesView(ListAPIView):
#     queryset = Article.objects.all().order_by('id')
#     serializer_class = ArticleSerializer
#     pagination_class = PageNumberPagination


class ArticlesView(GenericAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            article = self.get_object()
            serializer = self.serializer_class(article)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ArticlesAllAPI(ListAPIView):
    """
    This view will return response with full articles 
    (title, body, data, author, liked_by),
    but divided into 10 users objects at the one response.
    Used limit and offset.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleFullDataSerializer
    pagination_class = LimitOffsetPagination


class ArticleCreateAPI(APIView):
    """
    This view will check input user unique title name and then, 
    if data is valid, create new article
    and return success message
    """
    serializer_class = ArticleCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            # create new article and save in base
            new_article = Article.objects.create(
                title=validate_data.get('title'),
                body=validate_data.get('body'),
                author=request.user
            )
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class ArticleRemoveAPI(APIView):
    """
    This view will check if input user title is exist and then, 
    if data is valid,
    check if current user is author of article with request title.
    If check is correct, article with request title will be remove from base.
    """
    serializer_class = ArticleRemoveSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            article = Article.objects.get(title=validate_data.get('title'))
            # check if user is author of article with request title
            if article.author != request.user:
                raise ValidationError(
                    'Sorry, but you can\'t delete not your articles')
            # remove article with request title
            else:
                article.delete()
                return Response({'success': True})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ArticlesSearchAPI(APIView):
    """
    This view will found all articles by input user keyword in title and body,
    and return all of them.
    """
    serializer_class = ArticleSearchSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            keyword = serializer.validated_data.get('search_keyword')
            # filter by input user keyword in articles title and body
            articles = Article.objects.filter(
                Q(title__contains=keyword) | Q(body__contains=keyword))
            return Response(ArticleFullDataSerializer(
                articles, many=True).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
