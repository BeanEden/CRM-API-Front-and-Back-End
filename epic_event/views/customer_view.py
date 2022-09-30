from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import get_object_or_404, redirect, render

from django.views import View
from django.views.generic.list import ListView

from epic_event.models.event import Event
from epic_event.models.contract import Contract
from epic_event.models.customer import Customer
from epic_event.serializers import UserDetailSerializer
from epic_event.serializers import CustomerDetailSerializer
from epic_event.forms import CustomerForm, DeleteBlogForm

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from epic_event.views.general_view import PaginatedViewMixin
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
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
            # events = Event.objects.filter(support_contact=request.user)
            # queryset = Customer.objects.filter(customer_id_in=events.id)
            wanted_items = set()
            for item in Event.objects.filter(sales_contact=request.user):
                wanted_items.add(item.id)
            queryset = Customer.objects.filter(pk__in=wanted_items)
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



@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def customer_create_view(request):
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    if request.user.team == "sales":
        serializer = CustomerDetailSerializer(data={"sales_contact":request.user.id}, partial=True)
        if serializer.is_valid():
            return render(request, 'customer/customer_create.html',
                          context={'serializer': serializer})
    serializer = CustomerDetailSerializer()
    if request.method == 'POST':
        serializer = CustomerDetailSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            name = serializer.data["first_name"] +' '+ serializer.data["last_name"]
            flash = "Customer " + name + "has been created"
            return render(request, 'home.html', context={'flash': flash})
    return render(request, 'customer/customer_create.html',
                  context={'serializer': serializer})



@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def customer_detail_view(request, customer_id):
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    customer = get_object_or_404(Customer, id=customer_id)
    serializer = CustomerDetailSerializer(customer)
    if "update_customer" in request.POST:
        serializer = CustomerDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            name = str(customer)
            flash = "Customer " + name + " has been successfully updated"
            return render(request, 'home.html', context={'flash': flash})
    if "delete_customer" in request.POST:
        if request.user.team != "management":
            flash = "You don't have permission to access this page"
            return render(request, 'home.html', context={'flash': flash})
        name = customer
        customer.delete()
        flash = "Customer " + str(name) + " has been successfully deleted"
        return render(request, 'home.html', context={'flash': flash})
    return render(request, 'customer/customer_detail.html',
                  context={'serializer': serializer, 'customer': customer})

#
# @login_required
# def customer_delete(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#     delete_form = DeleteBlogForm()
#     if request.method == 'POST':
#         customer.delete()
#         return redirect('home')
#     context = {'customer': customer, 'delete_form': delete_form}
#     return render(request, 'customer/customer_delete.html', context=context)


    # delete_form = DeleteBlogForm()
    # if request.method == "POST":
    #     if request.user.team != 'management':
    #         flash = "You don't have permission to access this page"
    #         return render(request, 'home.html', context={'flash': flash})
    #     name = serializer.data["first_name"] + ' ' + serializer.data[
    #         "last_name"]
    #     serializer.delete()
    #     flash = "Customer " + name + "has been deleted"
    #     return render(request, 'home.html', context={'flash': flash})











class CustomerDetailView(APIView):

    permission_classes = [IsAuthenticated, IsManagementTeam]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/customer_detail.html'

    def get(self, request, pk, format = None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerDetailSerializer(customer)
        return Response({'serializer': serializer})

    def patch(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        print(customer)
        serializer = CustomerDetailSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # return Response({'serializer': serializer})
            return redirect('user_list')
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

# # @login_required
# def customer_create_view(request):
#     if request.user.team == "management":
#         return render(request, 'home.html',)
#     print("aaa")
#     serializer = CustomerDetailSerializer()
#     return render(request, 'customer/customer_create.html', context={'serializer': serializer})

    # print(request.user.team)
    # serializer['sales_contact'] = request.user.id
    # print(serializer)
    # print(serializer['sales_contact'])
    # # serializer['sales_contact'] =
    #
    # if request.method == 'POST':
    #     serializer = serializer.TicketForm(request.POST, request.FILES)
    #     if serializer.is_valid():
    #         ticket = serializer.save(commit=False)
    #         ticket.user = request.user
    #         ticket.save()
    #         return redirect('home')