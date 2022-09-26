from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

# from epic_event.views import SignUpView
from epic_event.views.user_view import UserListView, UserCreateDetailView, UserDetailView
from epic_event.views.customer_view import CustomerListView, CustomerCreateView, CustomerDetailView
from epic_event.views.contract_view import ContractListView, ContractCreateView, ContractDetailView
from epic_event.views.event_view import EventListView, EventCreateView, EventDetailView
import epic_event.views
from epic_event.views.general_view import GlobalFeed
from authentication.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),


    # -------------------------AUTHENTICATION PAGES-------------------------#

    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    # path('signup/', SignUpView.as_view(),
    #      name='signup'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
        name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
        name='password_change_done'),
    # --------------------------HOME AND USER PAGES--------------------------#

    path('home/', GlobalFeed.as_view(), name='home'),
    # path('event_list/', epic_event.views.EventListView.as_view(), name='event_list'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_create/', SignUpView.as_view(), name='user_create'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    # path('customer_create/', epic_event.views.CustomerCreateDetail.as_view(), name='customer_create')
    # path('contract_list/')
    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('customer_create/', CustomerCreateView.as_view(), name='customer_create'),
    path('contract_list:', ContractListView.as_view(), name='contract_list'),
    path('<int:pk>/contract_create/', ContractCreateView.as_view(), name='customer_contract_create'),
    path('<int:pk>/contract_list/', ContractCreateView.as_view(), name='customer_contract_list'),
    path('contract_create/', ContractCreateView.as_view(),
         name='contract_create'),
    path('event_list/', EventListView.as_view(), name = 'event_list'),
    path('event_create/', EventCreateView.as_view(), name= 'event_create')
    ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)