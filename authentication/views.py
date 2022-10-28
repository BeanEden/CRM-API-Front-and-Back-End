"""Sign up view"""
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer


class SignUpView(generic.CreateView):
    """Sign up view"""
    form_class = SignupForm
    success_url = reverse_lazy("token_obtain_pair")
    template_name = 'authentication/signup.html'


class MyObtainTokenPairView(TokenObtainPairView):
    """ Login View"""
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


