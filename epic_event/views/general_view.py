"""General pages views"""
from itertools import chain
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from epic_event.models.event import Event
from epic_event.models.contract import Contract
from epic_event.models.customer import Customer
from epic_event.controller.general_controller import search_event, \
    search_contract, \
    search_customer, search_user, get_last_posts_selected

from rest_framework.views import APIView


User = get_user_model()


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

    def get(self, request):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        query = request.GET.get('search')
        posts = get_last_posts_selected(query)
        posts_paged = self.paginate_view(
            request, sorted(posts,
                            key=lambda x: x.date_updated, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})


def search(request):
    """Global search result"""
    posts_paged = []
    query = ""
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        customers = search_customer(query)
        contracts = search_contract(query)
        events = search_event(query)
        users = search_user(query)
        posts_paged = sorted(chain(customers, contracts, events, users),
                             key=lambda x: x.date_updated, reverse=True)
    return render(request, 'home.html', {'query': query,
                                         'page_obj': posts_paged})


def search_customers(request):
    """Global search result"""
    posts_paged = []
    query = ""
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        customers = search_customer(query)
        posts_paged = sorted(customers,
                             key=lambda x: x.date_updated, reverse=True)
    return render(request, 'home.html', {'query': query,
                                         'page_obj': posts_paged})


def search_contracts(request):
    """Global search result"""
    posts_paged = []
    query = ""
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        contracts = search_contract(query)
        posts_paged = sorted(contracts,
                             key=lambda x: x.date_updated, reverse=True)
    return render(request, 'home.html', {'query': query,
                                         'page_obj': posts_paged})

def search_events(request):
    """Global search result"""
    posts_paged = []
    query = ""
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        events = search_event(query)
        posts_paged = sorted(events,
                             key=lambda x: x.date_updated, reverse=True)
    return render(request, 'home.html', {'query': query,
                                         'page_obj': posts_paged})


def search_users(request):
    """Global search result"""
    posts_paged = []
    query = ""
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        users = search_user(query)
        posts_paged = sorted(users,
                             key=lambda x: x.date_updated, reverse=True)
    return render(request, 'home.html', {'query': query,
                                         'page_obj': posts_paged})
