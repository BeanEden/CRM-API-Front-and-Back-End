from itertools import chain
from copy import deepcopy
from django.contrib.auth import get_user_model, forms

from django.shortcuts import get_object_or_404, redirect, render

from epic_event.models.event import Event
from epic_event.models.contract import Contract
from epic_event.models.customer import Customer
from epic_event.serializers import UserDetailSerializer
from epic_event.serializers import CustomerDetailSerializer

from epic_event.views.general_view import PaginatedViewMixin

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()

from rest_framework.permissions import IsAuthenticated, AllowAny, \
    IsAuthenticatedOrReadOnly
from epic_event.permissions import IsManagementTeam



class UserListView(APIView, PaginatedViewMixin):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_list.html'
    permission_classes = [IsAuthenticated, IsManagementTeam]


    def get(self, request):
        if request.user.team == "management":
            queryset = User.objects.all()
            serializer = UserDetailSerializer()
            posts_paged = self.paginate_view(
                request, sorted(queryset,
                                key=lambda x: x.username, reverse=False))
            # context = {'users': posts_paged, 'serializer': serializer}
            # render(request, self.template_name, context=context)
            return Response({'users': posts_paged, 'serializer': serializer})
        else :
            flash = "You don't have permission to access this page"
            return redirect('home')

    def post(self, request, format=None):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_detail.html'
    permission_classes = [IsAuthenticated, IsManagementTeam]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserDetailSerializer(user)
        return Response({'serializer': serializer, 'profile': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserDetailSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('user_detail')


class UserCreateDetailView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_create.html'
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = UserDetailSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)