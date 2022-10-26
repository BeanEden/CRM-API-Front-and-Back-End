"""Event controller"""
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from epic_event.models.event import Event
from epic_event.models.customer import Customer
from epic_event.serializers import EventSerializer, AdminEventSerializer
from .utilities import error_log


User = get_user_model()


def create_event(request, contract):
    """Docstring"""
    serializer = create_event_serializer(request=request)
    if serializer.is_valid():
        serializer.save()
        contract.event_associated = "complete"
        contract.save()
        event = get_object_or_404(Event, id=serializer.data['id'])
        flash = "Event " + str(event) + " has been successfully created"
        return render(request, 'event/event_read_only.html',
                      context={'flash': flash, 'serializer': serializer,
                               'event': event})
    error_log(request=request,
              text="unvalid serializer: " + str(serializer.errors))
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, "contract": contract})


def create_event_permission_redirect(request):
    """Redirect unauthorized user"""
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        error_log(request=request,
                              text="tried unauthorized event creation")
        return render(request, 'home.html', context={'flash': flash})
    return "authorized"


def create_event_check_contract_already_has_an_event_redirect(request,
                                                              contract):
    """Redirect if contract already have an event"""
    if contract.event_associated == "complete":
        flash = "This contract already has an event"
        error_log(request=request,
                              text=str(contract) +
                                   "contract already has an event")
        return render(request, 'home.html', context={'flash': flash})
    return "authorized"


def event_permission_redirect_read_only(request, event):
    """Redirect permission if user isn't authorized to update/delete events"""
    if request.user.team == "support" and \
            request.user != event.support_contact:
        return render(request, 'event/event_read_only.html',
                      context={'event': event})
    if request.user.team == "sales" and \
            request.user != event.contract_id.sales_contact:
        return render(request, 'event/event_read_only.html',
                      context={'event': event})
    return "authorized"


def event_read_only_toggle(request, context):
    """Docstring"""
    if request.POST['read_only'] == "update_mode_off":
        return render(request, 'event/event_read_only.html',
                      context=context)
    if request.POST['read_only'] == "update_mode_on":
        return render(request, 'event/event_detail.html',
                      context=context)
    return "authorized"


def update_event(request, event):
    """Docstring"""
    serializer = update_event_serializer(request=request, event=event)
    if serializer.is_valid():
        serializer.save()
        name = str(event)
        flash = name + " has been successfully updated"
        return render(request, 'event/event_read_only.html',
                      context={'flash': flash,
                               'serializer': serializer, 'event': event})
    error_log(request=request,
              text="unvalid serializer: " + str(serializer.errors))
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, 'event': event})


def delete_event(request, event):
    """Docstring"""
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        error_log(request=request,
                              text="tried unauthorized event deletion")
        return render(request, 'home.html', context={'flash': flash})
    name = str(event)
    event.delete()
    flash = name + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})


def create_event_serializer_filling(request, contract):
    """Docstring"""
    if request.user.team == "management":
        serializer = AdminEventSerializer(data={
            "customer_id": contract.customer_id.id,
            "contract_id": contract.id},
            partial=True)
        serializer.is_valid()
    else:
        serializer = EventSerializer()
    return serializer


def create_event_serializer(request):
    """Docstring"""
    if request.user.team == "management":
        serializer = AdminEventSerializer(data=request.data)

    else:
        serializer = EventSerializer(data=request.data)
    return serializer


def update_event_serializer_filling(request, event):
    """Docstring"""
    if request.user.team == "management":
        serializer = AdminEventSerializer(instance=event)

    else:
        serializer = EventSerializer(instance=event)
    return serializer


def update_event_serializer(request, event):
    """Docstring"""
    if request.user.team == "management":
        serializer = AdminEventSerializer(data=request.data, instance=event)

    else:
        serializer = EventSerializer(data=request.data, instance=event)
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
