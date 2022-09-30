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
from rest_framework import status

User = get_user_model()
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from epic_event.permissions import IsManagementTeam
from epic_event.views.general_view import PaginatedViewMixin


class EventListView(APIView, PaginatedViewMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
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


@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def event_create_view(request, contract_id=None):
    if request.user.team == "support":
        serializer = EventDetailSerializer(data={"support_contact": request.user.id}, partial=True)
        if serializer.is_valid():
            return render(request, 'event/event_create.html',
                          context={'serializer': serializer})
    serializer = EventDetailSerializer()
    if request.method == 'POST':
        serializer = EventDetailSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            flash = "Event " + str(serializer) + "has successfully been created"
            return render(request, 'home.html', context={'flash': flash})
    return render(request, 'event/event_create.html',
                  context={'serializer': serializer})


@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    serializer = EventDetailSerializer(event)
    if "update_event" in request.POST:
        serializer = EventDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            name = str(event)
            flash = name + " has been successfully updated"
            return render(request, 'home.html', context={'flash': flash})
    if "delete_contract" in request.POST:
        if request.user.team != "management":
            flash = "You don't have permission to access this page"
            return render(request, 'home.html', context={'flash': flash})
        name = str(event)
        event.delete()
        flash = name + " has been successfully deleted"
        return render(request, 'home.html', context={'flash': flash})
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, 'event': event})



class EventDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_detail.html'
    permission_classes = [IsAuthenticated, IsManagementTeam]

    def get(self, request, pk, format = None):
        customer = get_object_or_404(Event, pk=pk)
        serializer = EventDetailSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventDetailSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_create.html'
    permission_classes = [IsAuthenticated, IsManagementTeam]

    def get(self, request):
        serializer = EventDetailSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = EventDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
