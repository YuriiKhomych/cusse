from django.conf.urls import url

from events.views import events_list

urlpatterns = [
    url(r'^$', events_list, name='all_events'),
]
