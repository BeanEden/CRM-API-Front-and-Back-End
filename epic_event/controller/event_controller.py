"""Docstring"""
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from epic_event.models.event import Event
from epic_event.models.customer import Customer
from epic_event.serializers import EventDetailSerializer

User = get_user_model()


def create_event(request, contract):
    """Docstring"""
    serializer = EventDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        contract.event_associated = "complete"
        contract.save()
        print(contract)
        event = get_object_or_404(Event, id=serializer.data['id'])
        flash = "Event " + str(event) + " has been successfully created"
        return render(request, 'event/event_read_only.html',
                      context={'flash': flash, 'serializer': serializer,
                               'event': event})

    return render(request, 'event/event_create.html',
                  context={'serializer': serializer, "contract": contract})


def create_event_permission_redirect(request):
    """Docstring"""
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    return "good"


def create_event_check_contract_already_has_an_event_redirect(request,
                                                              contract):
    """Docstring"""
    if contract.event_associated == "complete":
        flash = "This contract already has an event"
        return render(request, 'home.html', context={'flash': flash})
    return "good"


def event_permission_redirect_read_only(request, event):
    """Docstring"""
    if request.user.team == "support" and \
            request.user != event.support_contact:
        return render(request, 'event/event_read_only.html',
                      context={'event': event})
    if request.user.team == "sales" and \
            request.user != event.contract_id.sales_contact:
        return render(request, 'event/event_read_only.html',
                      context={'event': event})
    return "good"


def event_read_only_toggle(request, context):
    """Docstring"""
    if request.POST['read_only'] == "update_mode_off":
        return render(request, 'event/event_read_only.html',
                      context=context)
    if request.POST['read_only'] == "update_mode_on":
        return render(request, 'event/event_detail.html',
                      context=context)
    return "good"


def update_event(request, event):
    """Docstring"""
    serializer = EventDetailSerializer(data=request.data, instance=event)
    if serializer.is_valid():
        serializer.save()
        name = str(event)
        flash = name + " has been successfully updated"
        return render(request, 'event/event_read_only.html',
                      context={'flash': flash,
                               'serializer': serializer, 'event': event})
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, 'event': event})


def delete_event(request, event):
    """Docstring"""
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    name = str(event)
    event.delete()
    flash = name + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})


def create_event_serializer_filling(contract):
    """Docstring"""
    serializer = EventDetailSerializer(data={
        "customer_id": contract.customer_id.id,
        "contract_id": contract.id},
        partial=True)
    serializer.is_valid()
    return serializer


def user_events_queryset(user):
    """Docstring"""
    if user.team == 'management':
        queryset = Event.objects.all()
    elif user.team == 'sales':
        wanted_items = set()
        for item in Customer.objects.filter(sales_contact=user):
            wanted_items.add(item.id)
        queryset = Event.objects.filter(pk__in=wanted_items)
    else:
        queryset = Event.objects.filter(support_contact=user)
    return queryset


def my_events_queryset(request):
    """Docstring"""
    if request.user.team == 'management':
        queryset = Event.objects.all()
    elif request.user.team == 'sales':
        wanted_items = set()
        for item in Customer.objects.filter(sales_contact=request.user):
            wanted_items.add(item.id)
        queryset = Event.objects.filter(pk__in=wanted_items)
    else:
        queryset = Event.objects.filter(support_contact=request.user)
    return queryset


def unassigned_event_queryset():
    """Docstring"""
    queryset = Event.objects.filter(support_contact=None)
    return queryset
