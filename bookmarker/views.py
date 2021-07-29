from rest_framework import permissions
from rest_framework import viewsets

from bookmarker.models import Bookmark, List
from bookmarker.serializers import BookmarkSerializer, ListSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkViewSet(ViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class ListViewSet(ViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
