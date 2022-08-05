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



class EventList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ""
        if request.user.team == 'management':
            queryset = Event.objects.all()
        if request.user.team == 'sales':
            wanted_items = set()
            for item in Contract.objects.filter(sales_contact=request.user):
                wanted_items.add(item.id)
            queryset = Event.objects.filter(pk__in=wanted_items)
        if request.user.team == 'support':
            queryset = Event.objects.filter(support_contact=request.user)
        return Response({'events': queryset})


class UserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_list.html'
    permission_classes = [IsAuthenticated, IsManagementTeam]

    def get(self, request):
        queryset = ""
        if request.user.team == 'management':
            queryset = User.objects.all()
        if request.user.team == 'sales':
            wanted_items = set()
            for item in Contract.objects.filter(sales_contact=request.user):
                wanted_items.add(item.id)
            queryset = Event.objects.filter(pk__in=wanted_items)
        if request.user.team == 'support':
            queryset = Event.objects.filter(support_contact=request.user)
        return Response({'users': queryset})

    # def

class UserDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_detail.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserDetailSerializer(user)
        return Response({'serializer': serializer, 'profile': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserDetailSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': user})
        serializer.save()
        return redirect('user_list')

# if pk: # the update request
#     conta = get_object_or_404(Conta, pk=pk, user=user)
#     serializer = ContaDetailsSerializerPosts(conta, data=request.data)
# else:  # the create request
#     serializer = ContaDetailsSerializerPosts(data=request.data)


class UserCreateDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_create.html'

    def get(self, request):
        serializer = UserDetailSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserDetailSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerCreateDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_create.html'

    def get(self, request):
        serializer = CustomerDetailSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------HOME AND USER PAGES---------------------------#

class GlobalFeed(LoginRequiredMixin, View, PaginatedViewMixin):
    """Class view used to generate a paginated list of all tickets and reviews
    ordered chronologically (soonest first)
    """
    template_name = 'home.html'

    def get(self, request):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """

        if request.user.team == 'support':
            events = Event.objects.filter(support_contact=request.user)

            posts_paged = self.paginate_view(
                request, sorted(events,
                                key=lambda x: x.date_updated, reverse=True))
            return render(request, self.template_name,
                          context={'page_obj': posts_paged})
        if request.user.team == 'sales':
            customers = Customer.objects.filter(sales_contact=request.user)
            contracts = Contract.objects.filter(sales_contact=request.user)

        if request.user.team == 'management':
            customers = Customer.objects.all()
            contracts = Contract.objects.all()
            events = Event.objects.all()
            posts_paged = self.paginate_view(
                request, sorted(chain(customers, contracts, events),
                                key=lambda x: x.date_updated, reverse=True))
            return render(request, self.template_name,
                          context={'page_obj': posts_paged})

