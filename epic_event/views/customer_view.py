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
from epic_event.views.general_view import PaginatedViewMixin

User = get_user_model()

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from epic_event.permissions import IsManagementTeam



class CustomerListView(APIView, PaginatedViewMixin):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_list.html'

    def get(self, request, format = None):
        serializer = CustomerDetailSerializer()
        if request.user.team == "management" or "sales":
            queryset = Customer.objects.all()
        elif request.user.team == "support":
            events = Event.objects.filter(support_contact=request.user)
            queryset = Customer.objects.filter(customer_id_in=events.id)
        else:
            flash = "You don't have permission to access this page"
            return redirect('home')
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'customers': posts_paged, 'serializer': serializer})


    def post(self, request, format=None):
        serializer = CustomerDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):

    permission_classes = [IsAuthenticated, IsManagementTeam]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_detail.html'

    def get(self, request, pk, format = None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerDetailSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerDetailSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerCreateView(APIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_create.html'

    def get(self, request):
        serializer = CustomerDetailSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = CustomerDetailSerializer(data=request.data)
        print("serializer ___>", serializer)
        print("serializer_valid", serializer.is_valid())
        print("serializer_error", serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
