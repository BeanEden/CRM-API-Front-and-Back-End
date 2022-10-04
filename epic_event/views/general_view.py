from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import get_object_or_404, redirect, render

from django.views import View
from django.views.generic.list import ListView

from epic_event.models.event import Event
from epic_event.models.contract import Contract
from epic_event.models.customer import Customer
from epic_event.serializers import UserDetailSerializer
from epic_event.serializers import CustomerDetailSerializer

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()

from rest_framework.permissions import IsAuthenticated, AllowAny
from epic_event.permissions import IsManagementTeam

# -----------------------------MIXINS-----------------------------#

class PaginatedViewMixin:
    """Mixin to paginate feeds class"""

    @staticmethod
    def paginate_view(request, object_paginated):
        """Method to paginate feed

        arguments: request, post _lit (ex: list of reviews)
        return: post_list paginated"""

        paginator = Paginator(object_paginated, 6)
        page = request.GET.get('page')
        try:
            object_paginated = paginator.page(page)
        except PageNotAnInteger:
            object_paginated = paginator.page(1)
        except EmptyPage:
            object_paginated = paginator.page(paginator.num_pages)
        return object_paginated





# ---------------------------HOME AND USER PAGES---------------------------#

class GlobalFeed(LoginRequiredMixin, APIView, PaginatedViewMixin):
    """Class view used to generate a paginated list of all tickets and reviews
    ordered chronologically (soonest first)
    """
    template_name = 'home.html'

    def get(self, request, **kwargs):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        customers = Customer.objects.all()
        contracts = Contract.objects.all()
        events = Event.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(chain(customers, contracts, events),
                            key=lambda x: x.date_updated, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})


class GlobalSearch(LoginRequiredMixin, APIView, PaginatedViewMixin):
    """Class view used to generate a paginated list of all tickets and reviews
    ordered chronologically (soonest first)
    """
    template_name = 'home.html'

    def get(self, request, **kwargs):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        customers = Customer.objects.all()
        contracts = Contract.objects.all()
        events = Event.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(chain(customers, contracts, events),
                            key=lambda x: x.date_updated, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})


# class GlobalFeed(LoginRequiredMixin, ListView, PaginatedViewMixin):
#     """Class view used to generate a paginated list of all tickets and reviews
#     ordered chronologically (soonest first)
#     """
#     template_name = 'home.html'
#
#     def get_queryset(self):
#         """
#         argument: GET request
#         return: url + page_object (= paginated posts)
#         """
#         print(self.request.query_para)
#         customers = Customer.objects.all()
#         contracts = Contract.objects.all()
#         events = Event.objects.all()
#         posts_paged = self.paginate_view(self.request,
#             sorted(chain(customers, contracts, events),
#                             key=lambda x: x.date_updated, reverse=True))
#         return posts_paged

#
# class GlobalFeed(LoginRequiredMixin, View, PaginatedViewMixin):
#     """Class view used to generate a paginated list of all tickets and reviews
#     ordered chronologically (soonest first)
#     """
#     template_name = 'home.html'
#
#     def get(self, request):
#         """
#         argument: GET request
#         return: url + page_object (= paginated posts)
#         """
#
#         if request.user.team == 'support':
#             events = Event.objects.filter(support_contact=request.user)
#
#             posts_paged = self.paginate_view(
#                 request, sorted(events,
#                                 key=lambda x: x.date_updated, reverse=True))
#             return render(request, self.template_name,
#                           context={'page_obj': posts_paged})
#         if request.user.team == 'sales':
#             customers = Customer.objects.filter(sales_contact=request.user)
#             contracts = Contract.objects.filter(sales_contact=request.user)
#             posts_paged = self.paginate_view(
#                 request, sorted(chain(customers, contracts),
#                                 key=lambda x: x.date_updated, reverse=True))
#             return render(request, self.template_name,
#                           context={'page_obj': posts_paged})
#
#         if request.user.team == 'management':
#             customers = Customer.objects.all()
#             contracts = Contract.objects.all()
#             events = Event.objects.all()
#             posts_paged = self.paginate_view(
#                 request, sorted(chain(customers, contracts, events),
#                                 key=lambda x: x.date_updated, reverse=True))
#             return render(request, self.template_name,
#                           context={'page_obj': posts_paged})