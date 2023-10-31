from django.shortcuts import render
from django.utils.translation import gettext as _


def home(request):
    context = {
        'title': _('home'),
    }
    return render(request, 'main/base.html', context)
