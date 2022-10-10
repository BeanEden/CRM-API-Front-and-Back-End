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



@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_permission_redirect_read_only(request=request, event=event)
    serializer = EventDetailSerializer(event)
    if "update_event" in request.POST:
        update_event(request=request, event=event, serializer=serializer)
    if "delete_event" in request.POST:
        delete_event(request=request, event=event)
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, 'event': event})


def create_event_permission_redirect(request):
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
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