"""User controller"""
from django.shortcuts import render
from epic_event.serializers import UserDetailSerializer


def user_permission_redirect_read_only(request, context):
    """Docstring"""
    if request.user.team != "management":
        return render(request, 'user/user_read_only.html',
                      context=context)
    return "authorized"


def user_read_only_toggle(request, context):
    """Docstring"""
    if request.POST['read_only'] == "update_mode_off":
        return render(request, 'event/event_read_only.html',
                      context=context)
    if request.POST['read_only'] == "update_mode_on":
        return render(request, 'event/event_detail.html',
                      context=context)
    return "authorized"


def update_user(request, user):
    """Docstring"""
    serializer = UserDetailSerializer(data=request.data, instance=user)
    if serializer.is_valid():
        serializer.save()
        name = str(user)
        flash = name + " has been successfully updated"
        return render(request, 'event/event_read_only.html',
                      context={'flash': flash,
                               'serializer': serializer, 'event': user})
    return render(request, 'event/event_detail.html',
                  context={'serializer': serializer, 'event': user})


def delete_user(request, user):
    """Docstring"""
    if request.user.team != "management":
        flash = "You don't have permission to access this page"
        return render(request, 'home.html', context={'flash': flash})
    name = str(user)
    user.delete()
    flash = name + " has been successfully deleted"
    return render(request, 'home.html', context={'flash': flash})
