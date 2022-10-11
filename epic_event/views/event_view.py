from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from epic_event.models.event import Event
from epic_event.models.contract import Contract
from epic_event.models.customer import Customer
from epic_event.serializers import EventDetailSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from epic_event.views.general_view import PaginatedViewMixin
from epic_event.controller.event_controller import create_event, \
    create_event_permission_redirect, \
    event_permission_redirect_read_only, \
    update_event, \
    delete_event,\
    create_event_check_contract_already_has_an_event_redirect


class EventListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Event.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'events': posts_paged})


class UserEventListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        if request.user.team == 'management':
            queryset = Event.objects.all()
        elif request.user.team == 'sales':
            wanted_items = set()
            for item in Customer.objects.filter(sales_contact=request.user):
                wanted_items.add(item.id)
            queryset = Event.objects.filter(pk__in=wanted_items)
        else:
            queryset = Event.objects.filter(support_contact=request.user)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'events': posts_paged})


class CustomerEventListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        queryset = Event.objects.filter(customer_id=customer_id)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'events': posts_paged})


class AttributeEventListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        queryset = Event.objects.filter(support_contact=None)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'events': posts_paged})


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required()
def event_create_view(request, contract_id):
    create_event_permission_redirect(request)
    contract = get_object_or_404(Contract, id=contract_id)
    create_event_check_contract_already_has_an_event_redirect(
        request=request,
        contract=contract)
    serializer = EventDetailSerializer(data={
        "customer_id": contract.customer_id.id,
        "contract_id": contract.id},
        partial=True)
    serializer.is_valid()
    serializer.get_extra_kwargs()
    if "create_event" in request.POST:
        return create_event(request=request, contract=contract)
    return render(request, 'event/event_create.html',
                  context={'serializer': serializer, "contract": contract})


@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_permission_redirect_read_only(request=request, event=event)
    serializer = EventDetailSerializer(event)
    if "update_event" in request.POST:
        return update_event(request=request, event=event)
    if "delete_event" in request.POST:
        return delete_event(request=request, event=event)
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, 'event': event})


@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def contract_event_detail_view(request, contract_id):
    event = get_object_or_404(Event, contract_id=contract_id)
    if request.user.team == "support":
        if request.user != event.support_contact :
            return (render(request, 'event/event_read_only.html', context={'event': event}))
    if request.user.team == "sales":
        if request.user != event.contract_id.sales_contact:
            return (render(request, 'event/event_read_only.html',
                           context={'event': event}))
    serializer = EventDetailSerializer(event)
    if "update_event" in request.POST:
        serializer = EventDetailSerializer(data=request.data, instance=event)
        if serializer.is_valid():
            serializer.save()
            name = str(event)
            flash = name + " has been successfully updated"
            return render(request, 'home.html', context={'flash': flash})
    if "delete_event" in request.POST:
        if request.user.team != "management":
            flash = "You don't have permission to access this page"
            return render(request, 'home.html', context={'flash': flash})
        name = str(event)
        event.delete()
        flash = name + " has been successfully deleted"
        return render(request, 'home.html', context={'flash': flash})
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, 'event': event})