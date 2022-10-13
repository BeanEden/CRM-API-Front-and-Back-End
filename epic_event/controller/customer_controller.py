from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from epic_event.serializers import CustomerDetailSerializer
from epic_event.models import Customer, Event


User = get_user_model()


def create_customer_permission_redirect(request):
    if request.user.team == "support":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    if request.user.team == "sales":
        serializer = CustomerDetailSerializer(data={"sales_contact":request.user.id}, partial=True,)
        if serializer.is_valid():
            return render(request, 'customer/customer_create.html',
                          context={'serializer': serializer})
    else:
        pass


def customer_permission_redirect_read_only(request, customer):
    if request.user.team == "support":
        return render(request, 'customer/customer_read_only.html', context={'customer': customer})
    else:
        pass


def create_customer(request):
    serializer = CustomerDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        customer = get_object_or_404(Customer, id=serializer.data['id'])
        customer.checking_profile_complete()
        print(customer.profile)
        name = serializer.data["first_name"] + ' ' + serializer.data["last_name"]
        flash = "Customer " + name + " has been successfully created"
        return render(request, 'home.html', context={'flash': flash})
    else:
        return render(request, 'customer/customer_create.html',
                      context={'serializer': serializer})


def update_customer(request, customer):
    serializer = CustomerDetailSerializer(data=request.data, instance=customer)
    if serializer.is_valid():
        serializer.save()
        customer.checking_profile_complete()
        print(customer.profile)
        name = str(customer)
        flash = "Customer " + name + " has been successfully updated"
        redirect('home', )
        return render(request, 'home.html', context={'flash': flash})
    else:
        return render(request, 'customer/customer_detail.html',
                      context={'serializer': serializer, 'customer': customer})


def delete_customer(request, customer):
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    name = customer
    customer.delete()
    flash = "Customer " + str(name) + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})


def user_customer_queryset(user):
    """Docstring"""
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
    """Docstring"""
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






