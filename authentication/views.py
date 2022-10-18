"""Sign up view"""
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm


class SignUpView(generic.CreateView):
    """Sign up view"""
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = 'authentication/signup.html'

