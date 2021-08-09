from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarker.models import Bookmark, EmailConfirmationToken, List, User
from bookmarker.serializers import BookmarkSerializer, ListSerializer, UserSerializer


class IsConfirmed(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_confirmed
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ViewSet(viewsets.ModelViewSet):
    # User must be logged in to use the API Viewsets. If the user is trying to modify
    # an existing object, they must also be associated with that object.
    permission_classes = [IsConfirmed, IsOwner]

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


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # pylint: disable=redefined-builtin, unused-argument
        user_serialized = UserSerializer(request.user)
        return Response(user_serialized.data)


@ensure_csrf_cookie
def set_csrf_cookie(request):
    return JsonResponse({"detail": "Cookie set"})


@require_POST
def login_user_view(request):
    data = request.POST
    email = data.get("email")
    password = data.get("password")
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"detail": "Success"})
    return JsonResponse({"detail": "Invalid email or password"}, status=400)


@require_POST
def register_user_view(request):
    data = request.POST
    email = str(data.get("email"))
    password = str(data.get("password"))
    try:
        validate_email(email)
        user = User.objects.create_user(email=email, password=password)
    except (ValidationError, ValueError) as e:
        return JsonResponse(
            {"detail": "Invalid email or password", "error": str(e)}, status=400
        )
    except IntegrityError:
        return JsonResponse(
            {"detail": "An account with this email already exists"}, status=400
        )
    login(request, user)
    send_user_confirmation(request, user)
    return JsonResponse({"detail": "Success"}, status=201)


@require_POST
def logout_user_view(request):
    logout(request)
    return JsonResponse({"detail": "Success"})


def send_user_confirmation(request, user):
    host = request.get_host()
    token = EmailConfirmationToken.objects.get_or_create(
        user=user, defaults={"token": get_random_string(length=100)}
    )[0]
    message_body = (
        f"Please go to this address to confirm your email:\nhttp://{host}"
        + reverse("confirm-user", kwargs={"user_id": user.id, "token_str": token})
    )
    send_mail(
        "Email Confirmation",
        message_body,
        f"noreply@{host}",
        [user.email],
    )


@require_POST
def resend_user_confirmation_view(request):
    if request.user.is_authenticated:
        send_user_confirmation(request, request.user)
        return JsonResponse({"detail": "Success"})
    return JsonResponse(
        {"detail": "Authentication credentials were not provided."}, status=403
    )


@require_GET
def confirm_user_view(request, user_id, token_str):
    user = (
        User.objects.filter(id=user_id)
        .filter(email_confirm_token__token=token_str)
        .first()
    )
    if user is None:
        raise Http404()
    user.is_confirmed = True
    user.save()
    return redirect("/confirmed/")


@require_GET
def get_user_confirmed_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"detail": request.user.is_confirmed})
    return JsonResponse(
        {"detail": "Authentication credentials were not provided."}, status=403
    )
