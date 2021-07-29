from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("bookmarks", views.BookmarkViewSet)
router.register("lists", views.ListViewSet)

urlpatterns = [path("", include(router.urls))]
