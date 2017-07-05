from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404, get_object_or_404

from blog.models import Article


def blogs(request):
    # data = {
    #     'first_name': 'John',
    #     'last_name': 'Smith'
    # }
    # return HttpResponse('qwjehgqwjkeh')
    # return HttpResponseRedirect('/qwertyui')
    # 'select * from blog_article' -> response -> django obj
    keyword = request.POST.get('keyword', '')
    articles = Article.objects.filter(title__contains=keyword)
    return render(request, 'blogs.html', {'articles': articles})


def single_blog(request, article_id):
    # try:
    #     # select * from blog_article where id = 2
    #     article = Article.objects.get(id=article_id)
    #     return render(request, 'single-blog.html', {'article': article})
    # except Article.DoesNotExist:
    #     raise Http404
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'single-blog.html', {'article': article})
