"""Controller function for contact views"""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from epic_event.views.general_view import PaginatedViewMixin
from epic_event.models.event import Event, Contract
from epic_event.serializers import ContractDetailSerializer


User = get_user_model()


class ContractListView(APIView, PaginatedViewMixin):
    """Global contract list view"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch all contracts"""
        queryset = Contract.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


class UserContractListView(APIView, PaginatedViewMixin):
    """Contract list of a user"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all contracts related to a user"""
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
            return redirect('home')
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


class CustomerContractListView(APIView, PaginatedViewMixin):
    """Contract list of a customer"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        """Get all contracts related to a customer"""
        queryset = Contract.objects.filter(customer_id=customer_id)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


def create_contract_permission_redirect(request):
    """Redirect if trying to create a contract while unauthorized"""
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    return "authorized to create a contract"


def create_contract_prefilled_serializer(request, customer):
    """Prefill the contract serializer form"""
    serializer = ContractDetailSerializer()
    if request.user.team == "sales":
        serializer = ContractDetailSerializer(data={
            "sales_contact": request.user.id,
            "customer_id": customer.id},
            partial=True)
        serializer.is_valid()
    if request.user.team == "management":
        serializer = ContractDetailSerializer(data={
            "sales_contact": customer.sales_contact,
            "customer_id": customer.id},
            partial=True)
        serializer.is_valid()
    return serializer


def contract_detail_context_with_event_or_not(serializer, contract):
    """Decide what context to use (if event associated)"""
    context = {}
    if contract.event_associated == "complete":
        event = get_object_or_404(Event, contract_id=contract)
        context = {'serializer': serializer, 'contract': contract,
                   'event': event}
    else:
        context = {'serializer': serializer, 'contract': contract}
    return context


def contract_read_only_permission_redirect(request, contract):
    """if unauthorized to udpdate/delete contract, redirect to read_only"""
    if request.user.team == "support":
        return render(request, 'contract/contract_read_only.html',
                      context={'contract': contract})
    if request.user.team == "sales" and request.user != contract.sales_contact:
        return render(request, 'contract/contract_read_only.html',
                      context={'contract': contract})
    return "authorized"


def contract_read_only_toggle(request, context):
    """toggle to redirect between update / read_only"""
    if request.POST['read_only'] == "update_mode_off":
        return render(request, 'contract/contract_read_only.html',
                      context=context)
    if request.POST['read_only'] == "update_mode_on":
        return render(request, 'contract/contract_detail.html',
                      context=context)
    return "toggle"


def create_contract(request, customer):
    """create contract_controller"""
    serializer = ContractDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        contract_list = Contract.objects.filter(
            customer_id=customer.id)
        customer.checking_status(contract_list)
        name = serializer.data["name"]
        flash = "Contract " + name + " with customer " + str(
            customer) + " has successfully been created"
        return render(request, 'home.html', context={'flash': flash})
    return render(request, 'contract/contract_create.html',
                  context={'serializer': serializer, 'customer': customer})


def update_contract(request, contract):
    """update contract controller"""
    serializer = ContractDetailSerializer(data=request.data, instance=contract)
    if serializer.is_valid():
        serializer.save()
        contract_list = Contract.objects.filter(
            customer_id=contract.customer_id)
        contract.customer_id.checking_status(contract_list)
        name = str(contract)
        flash = "Contract " + name + " has been successfully updated"
        return render(request, 'home.html', context={'flash': flash})
    context = contract_detail_context_with_event_or_not(
        serializer=serializer,
        contract=contract)
    return render(request, 'contract/contract_detail.html',
                  context=context)


def delete_contract(request, contract):
    """celete contract controller"""
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    name = contract
    contract.delete()
    flash = "Contract " + str(name) + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})


def user_contracts_queryset(user):
    """Select contracts of a specific user"""
    if user.team == 'management':
        queryset = Contract.objects.all()
    elif user.team == 'sales':
        queryset = Contract.objects.filter(sales_contact=user)
    else:
        wanted_items = set()
        for item in Event.objects.filter(support_contact=user):
            wanted_items.add(item.id)
        queryset = Contract.objects.filter(pk__in=wanted_items)
    return queryset


def my_contracts_queryset(request):
    """Select contracts of the connected user"""
    if request.user.team == 'management':
        queryset = Contract.objects.all()
    elif request.user.team == 'sales':
        queryset = Contract.objects.filter(sales_contact=request.user)
    else:
        wanted_items = set()
        for item in Event.objects.filter(support_contact=request.user):
            wanted_items.add(item.id)
        queryset = Contract.objects.filter(pk__in=wanted_items)
    return queryset
