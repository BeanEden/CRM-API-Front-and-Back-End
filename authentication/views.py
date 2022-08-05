from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm

from rest_framework.permissions import IsAuthenticated, AllowAny

from . import forms

from django.shortcuts import render


class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = 'authentication/signup.html'

