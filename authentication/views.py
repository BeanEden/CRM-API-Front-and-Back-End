"""Sign up view"""
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm


class SignUpView(generic.CreateView):
    """Sign up view"""
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = 'authentication/signup.html'

    # def post(self, request, *args, **kwargs):
    #     form = SignupForm(data=request.form)
    #     if form.is_valid:
    #         form.save()
    #     return reverse_lazy('login')
