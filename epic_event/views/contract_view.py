from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from epic_event.models import Event, Contract, Customer
from epic_event.serializers import ContractDetailSerializer
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

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class ContractListView(APIView, PaginatedViewMixin, LoginRequiredMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Contract.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})


class UserContractListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        queryset = user_contracts_queryset(user)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response(
            {'contracts': posts_paged})


class MyContractListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = my_contracts_queryset(request=request)
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


class NoEventContractListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'contract/contract_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Contract.objects.filter(event_associated="uncomplete")
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'contracts': posts_paged})



@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required()
def contract_create_view(request, customer_id):
    create_contract_permission_redirect(request=request)
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
    contract = get_object_or_404(Contract, id=contract_id)
    contract_read_only_permission_redirect(request=request, contract=contract)
    serializer = ContractDetailSerializer(contract)
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