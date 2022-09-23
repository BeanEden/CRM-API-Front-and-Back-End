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

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from epic_event.permissions import IsManagementTeam


class EventListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event/event_list.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ""
        if request.user.team == 'management':
            queryset = Event.objects.all()
        if request.user.team == 'sales':
            wanted_items = set()
            for item in Event.objects.filter(sales_contact=request.user):
                wanted_items.add(item.id)
            queryset = Event.objects.filter(pk__in=wanted_items)
        if request.user.team == 'support':
            queryset = Event.objects.filter(support_contact=request.user)
        return Response({'events': queryset})


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
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
