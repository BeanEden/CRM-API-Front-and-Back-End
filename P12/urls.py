from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

# from epic_event.views import SignUpView
from epic_event.views.user_view import UserListView, UserCreateDetailView, UserDetailView
from epic_event.views.customer_view import CustomerListView, CustomerCreateView, CustomerDetailView, customer_detail_view, customer_create_view
from epic_event.views.contract_view import ContractListView, ContractCreateView, ContractDetailView, contract_create_view,contract_detail_view
from epic_event.views.event_view import EventListView, EventCreateView, EventDetailView, event_create_view, event_detail_view
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

    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('customer_create/', customer_create_view, name="customer_create"),
    path('<int:customer_id>/customer_detail/', customer_detail_view,
         name="customer_detail"),

    path('contract_list/', ContractListView.as_view(), name='contract_list'),
    path('<int:customer_id>/contract_create/', contract_create_view,
             name='contract_create'),
    path('<int:contract_id>/contract_detail/', contract_detail_view, name='contract_detail'),
    path('contract_create/', contract_create_view,
                 name='contract_create_untied'),
    # path('<int:pk>/contract_create/', ContractCreateView.as_view(), name='customer_contract_create'),



    path('<int:pk>/contract_list/', ContractCreateView.as_view(), name='customer_contract_list'),


    path('event_list/', EventListView.as_view(), name = 'event_list'),
    path('<int:contract_id>/event_create/', event_create_view, name= 'event_create'),
    path('<int:event_id>/event_detail/', event_detail_view, name='event_detail'),
    path('event_create/', event_create_view,
         name='event_create_untied'),
    ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)