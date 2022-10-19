"""Contract view"""
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated

from epic_event.models import Contract, Customer
from epic_event.serializers import ContractSerializer
from epic_event.views.general_view import PaginatedViewMixin
from epic_event.controller.contract_controller import create_contract, \
    update_contract, \
    delete_contract, \
    contract_detail_context_with_event_or_not, \
    contract_read_only_toggle, \
    contract_read_only_permission_redirect, \
    create_contract_prefilled_serializer, \
    create_contract_permission_redirect, \
    my_contracts_queryset, \
    user_contracts_queryset

User = get_user_model()


class ContractListView(APIView, PaginatedViewMixin, LoginRequiredMixin):
    """All contracts view"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get all contracts"""
        queryset = Contract.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


class UserContractListView(APIView, PaginatedViewMixin):
    """All contracts of a user"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """get method"""
        user = get_object_or_404(User, id=user_id)
        queryset = user_contracts_queryset(user)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response(
            {'contracts': posts_paged})


class MyContractListView(APIView, PaginatedViewMixin):
    """All contracts related to the user"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get method"""
        queryset = my_contracts_queryset(request=request)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response(
            {'contracts': posts_paged})


class CustomerContractListView(APIView, PaginatedViewMixin):
    """All contracts related to a customer"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        """get method"""
        queryset = Contract.objects.filter(customer_id=customer_id)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


class NoEventContractListView(APIView, PaginatedViewMixin):
    """contract list with no event"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get method"""
        queryset = Contract.objects.filter(event_associated="uncomplete")
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required()
def contract_create_view(request, customer_id):
    """View of contract creation"""
    check = create_contract_permission_redirect(request=request)
    if check != "authorized":
        return check
    customer = get_object_or_404(Customer, id=customer_id)
    serializer = create_contract_prefilled_serializer(request=request,
                                                      customer=customer)
    if "create" in request.POST:
        return create_contract(request=request, customer=customer)
    return render(request, 'contract/contract_create.html',
                  context={'serializer': serializer, 'customer': customer})


@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required()
def contract_detail_view(request, contract_id):
    """Contract detail view (get / update/delete"""
    contract = get_object_or_404(Contract, id=contract_id)
    check = contract_read_only_permission_redirect(request=request, contract=contract)
    if check != "authorized":
        return check
    serializer = ContractSerializer(contract)
    context = contract_detail_context_with_event_or_not(serializer=serializer,
                                                        contract=contract)
    if "read_only" in request.POST:
        return contract_read_only_toggle(request=request,
                                         context=context)
    if "update_contract" in request.POST:
        return update_contract(request=request, contract=contract)
    if "delete_contract" in request.POST:
        return delete_contract(request=request, contract=contract)
    return render(request, 'contract/contract_detail.html',
                  context=context)
