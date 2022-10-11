from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from epic_event.serializers import CustomerDetailSerializer


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
    print("on")
    serializer = CustomerDetailSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer)
        name = serializer.data["first_name"] + ' ' + serializer.data["last_name"]
        flash = "Customer " + name + " has been successfully created"
        return render(request, 'home.html', context={'flash': flash})
    else:
        print(serializer.errors)
        pass


def update_customer(request, customer):
    serializer = CustomerDetailSerializer(data=request.data, instance=customer)
    if serializer.is_valid():
        serializer.save()
        name = str(customer)
        flash = "Customer " + name + " has been successfully updated"
        redirect('home', )
        return render(request, 'home.html', context={'flash': flash})
    else:
        print(serializer.errors)
        pass


def delete_customer(request, customer):
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    name = customer
    customer.delete()
    flash = "Customer " + str(name) + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})









