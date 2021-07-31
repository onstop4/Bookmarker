from rest_framework import permissions
from rest_framework import viewsets

from bookmarker.models import Bookmark, List
from bookmarker.serializers import BookmarkSerializer, ListSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ViewSet(viewsets.ModelViewSet):
    # User must be logged in to use the API Viewsets. If the user is trying to modify
    # an existing object, they must also be associated with that object.
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkViewSet(ViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        requested_list = self.request.query_params.get("list")
        requested_unread = self.request.query_params.get("unread")
        if requested_list is not None:
            queryset = queryset.filter(list=requested_list)
        if requested_unread == "1":
            queryset = queryset.filter(unread=True)
        elif requested_unread == "0":
            queryset = queryset.filter(unread=False)
        return queryset


class ListViewSet(ViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
