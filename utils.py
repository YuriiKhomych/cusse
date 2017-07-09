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
    if page_count > 10:
        if page_number <= 4:
            for key in range(1, 7):
                my_page.append(key)
            my_page.append('...')
            my_page.append(page_count)
        elif page_number >= (page_count - 4):
            my_page.append(1)
            my_page.append('...')
            for key in range((page_count - 5), page_count + 1):
                my_page.append(key)
        else:
            my_page.append(1)
            my_page.append('...')
            for key in range((page_number - 2), (page_number + 2)):
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