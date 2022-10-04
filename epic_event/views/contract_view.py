from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from epic_event.models.event import Event
from epic_event.models.contract import Contract
from epic_event.models.customer import Customer
from epic_event.serializers import UserDetailSerializer
from epic_event.serializers import CustomerDetailSerializer
from epic_event.serializers import ContractDetailSerializer, EventDetailSerializer

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, \
    IsAuthenticatedOrReadOnly
from epic_event.permissions import IsManagementTeam
from epic_event.views.general_view import PaginatedViewMixin


def get_path(request):
    path = request.path_info
    split_path = path.split('/')
    return split_path


class ContractListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Contract.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'events': posts_paged})


class UserContractListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.team == 'management':
            queryset = Contract.objects.all()
        elif request.user.team == "sales":
            queryset = Contract.objects.filter(sales_contact=request.user)
        elif request.user.team == "support":
            wanted_items = set()
            for item in Event.objects.filter(support_contact=request.user):
                wanted_items.add(item.id)
            queryset = Contract.objects.filter(pk__in=wanted_items)
        else:
            flash = "You don't have permission to access this page"
            return redirect('home')
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response(
            {'contracts': posts_paged})


class CustomerContractListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        queryset = Contract.objects.filter(customer_id=customer_id)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


class ContractDetailView(APIView):
    permission_classes = [IsAuthenticated, IsManagementTeam]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_detail.html'


    def get(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        serializer = ContractDetailSerializer(contract)
        return Response(serializer.data)

    def put(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        serializer = ContractDetailSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_create.html'

    def get(self, request):
        serializer = ContractDetailSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = ContractDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('event_create')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def contract_create_view(request, customer_id):
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    serializer = ContractDetailSerializer()
    customer = get_object_or_404(Customer, id=customer_id)
    if request.user.team == "sales":
        serializer = ContractDetailSerializer(data={
            "sales_contact": request.user.id,
            "customer_id": customer_id},
            partial=True)
        serializer.is_valid()
    if request.user.team == "management":
        serializer = ContractDetailSerializer(data={
            "sales_contact": customer.sales_contact.id,
            "customer_id": customer_id},
            partial=True)
        serializer.is_valid()
    if "create" in request.POST:
        serializer = ContractDetailSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            customer.status = 'ongoing'
            customer.save()
            name = serializer.data["name"]
            flash = "Contract " + name + "with customer" + str(customer) +" has been created"
            return render(request, 'home.html', context={'flash': flash})
    return render(request, 'contract/contract_create.html',
                  context={'serializer': serializer, 'customer':customer})


@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def contract_detail_view(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.user.team == "support":
        return render(request, 'contract/contract_read_only.html', context={'contract': contract})
    serializer = ContractDetailSerializer(contract)
    if "update_contract" in request.POST:
        serializer = ContractDetailSerializer(data=request.data, instance=contract)
        if serializer.is_valid():
            serializer.save()
            name = str(contract)
            flash = "Contract " + name + " has been successfully updated"
            return render(request, 'home.html', context={'flash': flash})
    if "delete_contract" in request.POST:
        if request.user.team != "management":
            flash = "You don't have permission to access this page"
            return render(request, 'home.html', context={'flash': flash})
        name = contract
        contract.delete()
        flash = "Contract " + str(name) + " has been successfully deleted"
        return render(request, 'home.html', context={'flash': flash})
    return render(request, 'contract/contract_detail.html',
                  context={'serializer': serializer, 'contract': contract})


# @api_view(('GET','POST'))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def contract_read_only_view(request, contract_id):
#     contract = get_object_or_404(Contract, id=contract_id)
#     return render(request, 'contract/contract_detail.html',
#                   context={'contract': contract})