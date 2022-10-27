"""Event view"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated

from epic_event.models import Event, Contract
from epic_event.views.general_view import PaginatedViewMixin
from epic_event.controller.event_controller import create_event, \
    create_event_permission_redirect, \
    event_permission_redirect_read_only, \
    update_event, \
    delete_event,\
    create_event_check_contract_already_has_an_event_redirect, \
    event_read_only_toggle, \
    user_events_queryset, \
    unassigned_event_queryset, \
    my_events_queryset, \
    create_event_serializer_filling, update_event_serializer_filling


User = get_user_model()


class EventListView(APIView, PaginatedViewMixin):
    """All events list"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Docstring"""
        queryset = Event.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        context = {'events': posts_paged,
                   'title': 'All events list'}
        return Response(context)


class UserEventListView(APIView, PaginatedViewMixin):
    """All events related to a user"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """Docstring"""
        user = get_object_or_404(User, id=user_id)
        queryset = user_events_queryset(user)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        context = {'events': posts_paged, 'title': 'Events list - ' +
                                                   str(user)}
        return Response(context)


class MyEventListView(APIView, PaginatedViewMixin):
    """All events related to the logged user"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Docstring"""
        queryset = my_events_queryset(request)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        context = {'events': posts_paged, 'title': 'Events list - '+ str(request.user)}
        return Response(context)


class CustomerEventListView(APIView, PaginatedViewMixin):
    """All events related to the customer"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        """Docstring"""
        queryset = Event.objects.filter(customer_id=customer_id)
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'events': posts_paged})


class UnassignedEventListView(APIView, PaginatedViewMixin):
    """All unassigned events list"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Docstring"""
        queryset = unassigned_event_queryset()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.date_updated, reverse=False))
        return Response({'events': posts_paged, 'title': "Events unassigned"})


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@login_required()
def event_create_view(request, contract_id):
    """Docstring"""
    check = create_event_permission_redirect(request)
    if check != "authorized":
        return check
    contract = get_object_or_404(Contract, id=contract_id)
    check = create_event_check_contract_already_has_an_event_redirect(
        request=request,
        contract=contract)
    if check != "authorized":
        return check
    serializer = create_event_serializer_filling(request=request, contract=contract)
    if "create" in request.POST:
        return create_event(request=request, contract=contract)
    return render(request, 'event/event_create.html',
                  context={'serializer': serializer, "contract": contract})


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def event_detail_view(request, event_id):
    """Event detail view (get, update, delete"""
    event = get_object_or_404(Event, id=event_id)
    check = event_permission_redirect_read_only(request=request, event=event)
    if check != "authorized":
        return check
    serializer = update_event_serializer_filling(request=request, event=event)
    context = {'serializer': serializer, 'event': event}
    if "read_only" in request.POST:
        return event_read_only_toggle(request=request, context=context)
    if "update_event" in request.POST:
        return update_event(request=request, event=event)
    if "delete_event" in request.POST:
        return delete_event(request=request, event=event)
    return render(request, 'event/event_detail.html',
                  context=context)


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def contract_event_detail_view(request, contract_id):
    """Event detail linked to a contract"""
    event = get_object_or_404(Event, contract_id=contract_id)
    check = event_permission_redirect_read_only(request=request, event=event)
    if check != "authorized":
        return check
    serializer = update_event_serializer_filling(request=request, event=event)
    context = {'serializer': serializer, 'event': event}
    if "read_only" in request.POST:
        return event_read_only_toggle(request=request, context=context)
    if "update_event" in request.POST:
        return update_event(request=request, event=event)
    if "delete_event" in request.POST:
        return delete_event(request=request, event=event)
    return render(request, 'event/event_detail.html',
                  context=context)
