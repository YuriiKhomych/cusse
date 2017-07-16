from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from accounts.models import User
from events.models import Event

from utils import gen_page_list


def events_list(request):
    event = Event.objects.all()
    # event.members.add()
    # event.members.add(User.objects.get(email='test@gmail.com'))
    # event.members.remove(User.objects.get(email='test@gmail.com'))
    # event.save()
    # print(event.title)
    # event.title = 'new title'
    # event.save()
    # print(event.title)
    # print(event.date)
    # members = event.members.all()
    # for member in members:
    #     print(member.email)
    page = request.GET.get('page', 1)
    p = Paginator(event, 1)
    try:
        final_events = p.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        final_events = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        final_events = p.page(p.num_pages)
    return render(request, 'events.html', {'events': final_events,
                                          'pagination': gen_page_list(page,p.num_pages)})

def single_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'single-event.html', {'event': event})

