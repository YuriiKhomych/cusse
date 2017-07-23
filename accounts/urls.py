from django.conf.urls import url

from accounts.views import all_users, single_user, sign_in, sign_out, sign_up, get_user_django, get_user_rest, change_user_password, ChangeUserPasswordView, MainUserFieldsView

urlpatterns = [
    url(r'^sign-in/$', sign_in, name='sign_in'),
    url(r'^sign-out/$', sign_out, name='sign_out'),
    url(r'^sign-up/$', sign_up, name='sign_up'),
    url(r'^users/$', all_users, name='all_users'),
    url(r'^single/(?P<user_id>\d+)/$', single_user, name='single_user_page'),
    url(r'^get-user-django/$', get_user_django),
    url(r'^get-user-rest/$', get_user_rest),
    url(r'^change-user-password/$', change_user_password),
    url(r'^change-user-password-rest/$', ChangeUserPasswordView.as_view()),
    url(r'^main-user-info/$', MainUserFieldsView.as_view()),
]


