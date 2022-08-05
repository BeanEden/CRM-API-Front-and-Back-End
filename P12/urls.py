from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

from authentication.views import SignUpView
import epic_event.views
from rest_framework import routers


urlpatterns = [
    path('admin/', admin.site.urls),


    # -------------------------AUTHENTICATION PAGES-------------------------#

    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    path('signup/', SignUpView.as_view(),
         name='signup'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
        name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
        name='password_change_done'),
    # --------------------------HOME AND USER PAGES--------------------------#

    path('home/', epic_event.views.GlobalFeed.as_view(), name='home'),
    path('event_list/', epic_event.views.EventList.as_view(), name='event_list'),
    path('user_list/', epic_event.views.UserList.as_view(), name='user_list'),
    path('user_create/', epic_event.views.UserCreateDetail.as_view(), name='user_create'),
    path('user_detail/<int:pk>/', epic_event.views.UserDetail.as_view(), name='user_detail'),
    path('customer_create/', epic_event.views.CustomerCreateDetail.as_view(), name='customer_create')
    # path('contract_list/')

    ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)