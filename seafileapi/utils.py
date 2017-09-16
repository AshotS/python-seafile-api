import string
import random
from datetime import datetime
from functools import wraps
from urllib import parse
from seafileapi.exceptions import ClientHttpError, DoesNotExist


def randstring(length=0):
    """

    :param length:
    :return:
    """
    if length == 0:
        length = random.randint(1, 30)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def urljoin(base, *args):
    """

    :param base:
    :param args:
    :return:
    """
    url = base
    if url[-1] != '/':
        url += '/'
    for arg in args:
        arg = arg.strip('/')
        url += arg + '/'
    if '?' in url:
        url = url[:-1]
    return url


def raise_does_not_exist(msg):
    """Decorator to turn a function that get a http 404 response to a
    :exc:`DoesNotExist` exception."""

    def decorator(func):
        """

        :param func:
        :return:
        """

        @wraps(func)
        def wrapped(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            try:
                return func(*args, **kwargs)
            except ClientHttpError as e:
                if e.code == 404:
                    raise DoesNotExist(msg)
                else:
                    raise

        return wrapped

    return decorator


def querystr(**kwargs):
    """

    :param kwargs:
    :return:
    """
    return '?' + parse.urlencode(kwargs)


def tsstr_sec(value):
    """Turn a timestamp to string"""
    try:
        return datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return datetime.fromtimestamp(value / 1000000).strftime("%Y-%m-%d %H:%M:%S")
