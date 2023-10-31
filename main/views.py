from django.shortcuts import render
from django.utils.translation import gettext as _

from .models import Hotel

def home(request):
    context = {
        'title': _('home'),
    }
    return render(request, 'main/home.html', context)
