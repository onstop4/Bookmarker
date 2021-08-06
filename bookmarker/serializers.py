from rest_framework import serializers

from bookmarker.models import Bookmark, List, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_confirmed"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "name", "url", "unread", "list"]

    def validate_list(self, value):
        user = self.context["request"].user
        if value is None or value.user == user:
            return value
        raise serializers.ValidationError("List does not belong to user")


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ["id", "name"]
