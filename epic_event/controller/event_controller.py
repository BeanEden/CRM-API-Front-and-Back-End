from itertools import chain

from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404, redirect, render

from epic_event.models.event import Event
from epic_event.models.contract import Contract
from epic_event.models.customer import Customer
from epic_event.serializers import UserDetailSerializer
from epic_event.serializers import CustomerDetailSerializer
from epic_event.serializers import EventDetailSerializer

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status

User = get_user_model()
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from epic_event.permissions import IsManagementTeam
from epic_event.views.general_view import PaginatedViewMixin


def create_event(request, contract):
    serializer = EventDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        contract.event_associated = "complete"
        contract.save()
        flash = "Event " + str(serializer) + " has been successfully created"
        return render(request, 'home.html', context={'flash': flash})
    else:
        pass


def create_event_permission_redirect(request):
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    else:
        pass


def create_event_check_contract_already_has_an_event_redirect(request, contract):
    if contract.event_associated == "complete":
        flash = "This contract already has an event"
        return render(request, 'home.html', context={'flash': flash})
    else:
        pass


def event_permission_redirect_read_only(request, event):
    if request.user.team == "support":
        if request.user != event.support_contact :
            return (render(request, 'event/event_read_only.html', context={'event': event}))
    elif request.user.team == "sales":
        if request.user != event.contract_id.sales_contact:
            return (render(request, 'event/event_read_only.html',
                           context={'event': event}))
    else:
        pass


def update_event(request, event):
    serializer = EventDetailSerializer(data=request.data, instance=event)
    if serializer.is_valid():
        # serializer.validated_data()
        serializer.save()
        name = str(event)
        flash = name + " has been successfully updated"
        return render(request, 'home.html', context={'flash': flash})
    else:
        pass


def delete_event(request, event):
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    name = str(event)
    event.delete()
    flash = name + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})

def create_event_serializer_filling(request, contract):
    serializer = EventDetailSerializer(data={
        "customer_id": contract.customer_id.id,
        "contract_id": contract.id},
        partial=True)
    serializer.is_valid()
    serializer.extr
    serializer.get_extra_kwargs(extra_kwargs = {"customer_id":{'read_only':True}})

    return serializer