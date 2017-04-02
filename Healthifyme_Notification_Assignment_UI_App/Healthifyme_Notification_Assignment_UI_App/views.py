__author__ = 'aaraokar'
import os
from django.http import HttpResponse
from django.template import *


def showNotificationUI(request):
    fp = open(os.path.join(os.path.dirname(__file__), 'static', 'index.html').replace('\\', '/'))
    t = Template(fp.read())
    html = t.render(Context())
    fp.close()
    return HttpResponse(html)
