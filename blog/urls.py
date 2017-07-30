from django.conf.urls import url

from blog.views import blogs, single_blog, user_articles, like_article,\
    send_email_rest, ArticlesView, ArticlesAllAPI,ArticleCreateAPI, \
    ArticleRemoveAPI, ArticlesSearchAPI

urlpatterns = [
    url(r'^$', blogs, name='all_articles'),
    url(r'^single/(?P<article_id>\d+)/$', single_blog,
        name='single_article_page'),
    url(r'^single/(?P<article_id>\d+)/like/$', like_article,
        name='like_article'),
    url(r'^user/(?P<user_id>\d+)/$', user_articles,
        name='user_articles'),

    url(r'^send-email-rest/$', send_email_rest, name='send_email_rest'),
    url(r'^articles-rest/$', ArticlesView.as_view()),
    url(r'^articles-rest/(?P<pk>\d+)/$', ArticlesView.as_view()),

    # rest framework
    url(r'^articles-all-api/$', ArticlesAllAPI.as_view()),
    url(r'^articles-create-api/$', ArticleCreateAPI.as_view()),
    url(r'^articles-remove-api/$', ArticleRemoveAPI.as_view()),
    url(r'^articles-search-api/$', ArticlesSearchAPI.as_view()),
]


# /blog/ -> all blogs
# /blog/single/12345/ -> single blog
# /blog/user/123456/ -> single user(with all articles)