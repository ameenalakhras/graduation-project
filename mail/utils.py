import urllib
from django.urls import reverse


def build_url(*args, **kwargs):
    parameters = kwargs.pop('pars', {})
    url = reverse(*args, **kwargs)
    if parameters:
        url += '?' + urllib.parse.urlencode(parameters)
    return url
