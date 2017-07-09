from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.models import Article

from utils import gen_page_list


def blogs(request):
    # data = {
    #     'first_name': 'John',
    #     'last_name': 'Smith'
    # }
    # return HttpResponse('qwjehgqwjkeh')
    # return HttpResponseRedirect('/qwertyui')
    # 'select * from blog_article' -> response -> django obj
    # keyword = request.POST.get('keyword', '')
    page = request.GET.get('page', 1)
    p = Paginator(Article.objects.all(), 1)
    try:
        final_articles = p.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        final_articles = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        final_articles = p.page(p.num_pages)
    return render(request, 'blogs.html', {'articles': final_articles,
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