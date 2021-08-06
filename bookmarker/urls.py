from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("bookmarks", views.BookmarkViewSet)
router.register("lists", views.ListViewSet)

urlpatterns = [
    path(
        "confirm/<int:user_id>/<token_str>/",
        views.confirm_user_view,
        name="confirm-user",
    ),
    path("api/user/", views.UserView.as_view()),
    path("api/resend-confirmation/", views.resend_user_confirmation_view),
    path("api/set-cookie/", views.set_csrf_cookie),
    path("api/login/", views.login_user_view),
    path("api/logout/", views.logout_user_view),
    path("api/register/", views.register_user_view),
    path("api/confirmed-status/", views.get_user_confirmed_status),
    path("api/", include(router.urls)),
]
