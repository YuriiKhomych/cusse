from django.conf.urls import url

from blog.views import blogs, single_blog

urlpatterns = [
    url(r'^$', blogs, name='all_articles'),
    url(r'^single/(?P<article_id>\d+)/$', single_blog, name='single_article_page')
]


# /blog/ -> all blogs
# /blog/single/sdjkghsdjkghdskjgh/ -> single blog