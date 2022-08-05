from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput,
                               label='Mot de passe')


USER_TEAM = [('management', 'GESTION'),
             ('sales', 'VENTE'),
             ('support', 'SUPPORT')]


class SignupForm(UserCreationForm):

    team = forms.ChoiceField(choices=USER_TEAM)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'team')

class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)