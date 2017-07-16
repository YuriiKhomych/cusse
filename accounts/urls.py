from django.conf.urls import url

from accounts.views import all_users, single_user, sign_in, sign_out, sign_up

urlpatterns = [
    url(r'^sign-in/$', sign_in, name='sign_in'),
    url(r'^sign-out/$', sign_out, name='sign_out'),
    url(r'^sign-up/$', sign_up, name='sign_up'),
    url(r'^users/$', all_users, name='all_users'),
    url(r'^single/(?P<user_id>\d+)/$', single_user, name='single_user_page'),
]


