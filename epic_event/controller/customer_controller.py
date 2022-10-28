"""Customer controller"""
from itertools import chain
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from epic_event.serializers import CustomerSerializer, AdminCustomerSerializer
from epic_event.models import Customer, Event


User = get_user_model()


# List queryset

def user_customer_queryset(user):
    """Customer queryset of a specific user"""
    if user.team == 'management':
        queryset = Customer.objects.all()
    elif user.team == 'sales':
        queryset = Customer.objects.filter(sales_contact=user)
    else:
        wanted_items = set()
        for item in Event.objects.filter(support_contact=user):
            wanted_items.add(item.id)
        queryset = Customer.objects.filter(pk__in=wanted_items)
    return queryset


def my_customers_queryset(request):
    """Customer queryset of the request.user"""
    if request.user.team == 'management':
        queryset = Customer.objects.all()
    elif request.user.team == 'sales':
        queryset = Customer.objects.filter(sales_contact=request.user)

    else:
        wanted_items = set()
        for item in Event.objects.filter(support_contact=request.user):
            wanted_items.add(item.id)
        queryset = Customer.objects.filter(pk__in=wanted_items)
    return queryset


def unactive_customers_queryset():
    """Customer queryset of the request.user"""
    prospects = Customer.objects.filter(status='prospect')
    unactive = Customer.objects.filter(status='unactive')
    queryset = chain(prospects, unactive)
    return queryset


# Create

def create_customer_permission_redirect(request):
    """Redirect unauthorized user"""
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    return "authorized"


def customer_serializer_choice_create(request):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminCustomerSerializer()
    else:
        serializer = CustomerSerializer()
    return serializer


def customer_serializer_choice_create_prefill(request):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminCustomerSerializer(data=request.data)
    else:
        serializer = CustomerSerializer(data=request.data)
    return serializer


def create_customer(request):
    """Create a customer controller"""
    serializer = customer_serializer_choice_create_prefill(request)
    if serializer.is_valid():
        serializer.save()
        customer = get_object_or_404(Customer, id=serializer.data['id'])
        if request.user.team == "sales":
            customer.sales_contact = request.user
            customer.save()
        customer.checking_profile_complete()
        name = serializer.data["first_name"] + ' ' + serializer.data["last_name"]
        flash = "Customer " + name + " has been successfully created"
        return render(request, 'home.html', context={'flash': flash})
    return render(request, 'customer/customer_create.html',
                  context={'serializer': serializer})


# Read

def customer_permission_redirect_read_only(request, customer):
    """Redirect unauthorized user to read only"""
    if request.user.team == "support":
        return render(request, 'customer/customer_read_only.html',
                      context={'customer': customer})
    return "authorized"


def customer_read_only_toggle(request, context):
    """Docstring"""
    if request.POST['read_only'] == "update_mode_off":
        return render(request, 'customer/customer_read_only.html',
                      context=context)
    if request.POST['read_only'] == "update_mode_on":
        return render(request, 'customer/customer_detail.html',
                      context=context)
    return "authorized"


# Update

def customer_serializer_choice_update_prefill(request, customer):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminCustomerSerializer(instance=customer)
    else:
        serializer = CustomerSerializer(instance=customer)
    return serializer


def customer_serializer_choice_update_save(request, customer):
    """Decides which serializer to pick regular or admin """
    if request.user.team == "management":
        serializer = AdminCustomerSerializer(data=request.data,
                                             instance=customer)
    else:
        serializer = CustomerSerializer(data=request.data, instance=customer)
    return serializer


def update_customer(request, customer):
    """Update customer controller"""
    serializer = customer_serializer_choice_update_save(request=request,
                                                        customer=customer)
    if serializer.is_valid():
        serializer.save()
        customer.checking_profile_complete()
        name = str(customer)
        flash = "Customer " + name + " has been successfully updated"
        return render(request, 'home.html', context={'flash': flash})
    return render(request, 'customer/customer_detail.html',
                  context={'serializer': serializer, 'customer': customer})


# Delete

def delete_customer(request, customer):
    """Delete customer"""
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    name = customer
    customer.delete()
    flash = "Customer " + str(name) + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})




