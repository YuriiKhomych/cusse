from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.core.mail import EmailMessage

import os
import uuid
import random
import string


def get_file_path(instance, filename):
    # instance = Article
    # filename = image.png
    ext = filename.split('.')[-1]  # .png
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)  # 2d4c673e339e4dd38037e91ad5ccd8a4.png
    return os.path.join(instance.__class__.__name__.lower(), filename)  # article/2d4c673e339e4dd38037e91ad5ccd8a4.png


def gen_page_list(page_number, page_count):
    page_number = int(page_number)
    # page_number = 3
    # page_count = 11
    my_page = []
    if page_count > 5:
        if page_number <= 4:
            for key in range(1, 5):
                my_page.append(key)
            my_page.append('...')
            my_page.append(page_count)
        elif page_number >= (page_count - 4):
            my_page.append(1)
            my_page.append('...')
            for key in range((page_count - 3), page_count + 1):
                my_page.append(key)
        else:
            my_page.append(1)
            my_page.append('...')
            for key in range((page_number - 1), (page_number + 2)):
                my_page.append(key)
            my_page.append('...')
            my_page.append(page_count)
    else:
        for key in range(0, page_count):
            my_page.append(key + 1)
    # 1, 2, 3, 4, 5, 6, 7, 8, 9
    # 1, 2, 3, 4, 5, 6, 7, ..., 11
    # 1, ..., 9, 10, 11
    # 1, ..., N, N, N, N, N ... 11
    return my_page


def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def build_url(*args, **kwargs):
    """
    Reverse func with optional get params
    """
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urllib.parse.urlencode(get)
    return url


def send_email(subject, user, template, content):
    ctx = {
        'first_name': content.get('first_name'),
        'last_name': content.get('last_name'),
    }
    from_email = "no-reply@klickjam.com"
    reply_to = "qweqwe"
    message = get_template(template).render(ctx)
    msg = EmailMessage(subject, message, from_email=from_email, bcc=[user], reply_to=[reply_to])
    msg.content_subtype = 'html'
    msg.send()
