from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('users:login')
