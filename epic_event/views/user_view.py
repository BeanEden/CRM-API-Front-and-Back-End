"""User views (except signup)"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from epic_event.permissions import IsManagementTeam
from epic_event.serializers import UserDetailSerializer
from epic_event.controller.user_controller import delete_user, update_user, \
    user_permission_redirect_read_only, user_read_only_toggle
from epic_event.views.general_view import PaginatedViewMixin


User = get_user_model()


class UserListView(APIView, PaginatedViewMixin):
    """All user list"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_list.html'
    permission_classes = [IsAuthenticated, IsManagementTeam]


    def get(self, request):
        """Get method"""
        queryset = User.objects.all()
        serializer = UserDetailSerializer()
        posts_paged = self.paginate_view(
            request, sorted(queryset,
                            key=lambda x: x.username, reverse=False))
        return Response({'users': posts_paged, 'serializer': serializer})


@api_view(('GET', 'POST', 'DELETE'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def user_detail_view(request, user_id):
    """User detail view"""
    user = get_object_or_404(User, id=user_id)
    serializer = UserDetailSerializer(user)
    context = {'user': user, 'serializer': serializer}
    check = user_permission_redirect_read_only(request=request, context=context)
    if check != "authorized":
        return check
    if "read_only" in request.POST:
        return user_read_only_toggle(request=request, context=context)
    if "update_user" in request.POST:
        return update_user(request=request, user=user)
    if "delete_event" in request.POST:
        return delete_user(request=request, user=user)
    return render(request, 'user/user_detail.html',
                  context=context)
