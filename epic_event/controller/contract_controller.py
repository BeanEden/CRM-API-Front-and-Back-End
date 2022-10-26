"""Controller function for contact views"""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from epic_event.views.general_view import PaginatedViewMixin
from epic_event.models.event import Event, Contract
from epic_event.serializers import ContractSerializer, AdminContractSerializer
from epic_event.controller.utilities import error_log


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


def create_contract_permission_redirect(request):
    """Redirect if trying to create a contract while unauthorized"""
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        error_log(request=request,
                  text="tried unauthorized contract creation")
        return render(request, 'home.html', context={'flash': flash})
    return "authorized"


def create_contract_prefilled_serializer(request, customer):
    """Prefill the contract serializer form"""
    serializer = ContractSerializer()
    if request.user.team == "management":
        serializer = AdminContractSerializer(data={
            "sales_contact": customer.sales_contact,
            "customer_id": customer.id},
            partial=True)
        serializer.is_valid()
    return serializer


def contract_serializer_choice(request):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminContractSerializer()
    else:
        serializer = ContractSerializer()
    return serializer

def contract_serializer_choice_create_prefill(request):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminContractSerializer(data=request.data)
    else:
        serializer = ContractSerializer(data=request.data)
    return serializer


def contract_serializer_choice_update_prefill(request, contract):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminContractSerializer(instance=contract)
    else:
        serializer = ContractSerializer(instance=contract)
    return serializer


def contract_serializer_choice_update(request, contract):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminContractSerializer(data=request.data,
                                             instance=contract)
    else:
        serializer = ContractSerializer(data=request.data, instance=contract)
    return serializer


def contract_detail_context_with_event_or_not(serializer, contract):
    """Decide what context to use (if event associated)"""
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
    serializer = AdminContractSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        if request.user.team == "sales":
            contract = Contract.objects.filter(id=serializer.data['id'])
            contract.sales_contact = customer.sales_contact.id
            contract.customer_id = customer
        contract_list = Contract.objects.filter(
            customer_id=customer.id)
        customer.checking_status(contract_list)
        name = serializer.data["name"]
        flash = "Contract " + name + " with customer " + str(
            customer) + " has successfully been created"
        return render(request, 'home.html', context={'flash': flash})
    serializer = create_contract_prefilled_serializer(request=request,
                                                      customer=customer)
    return render(request, 'contract/contract_create.html',
                  context={'serializer': serializer, 'customer': customer})


def update_contract(request, contract):
    """update contract controller"""
    serializer = contract_serializer_choice_update(request, contract)
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
        error_log(request=request,
                  text="tried unauthorized contract deletion")
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
