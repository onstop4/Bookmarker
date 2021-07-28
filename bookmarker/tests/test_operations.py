from django.test import TestCase

from bookmarker.models import User, List, Bookmark


class DeletionTests(TestCase):
    def test_user_delete(self):
        user = User.objects.create_user("test@example.com", "12345")
        list1 = List.objects.create(user=user, name="Test")
        list2 = List.objects.create(user=user, name="Test")
        Bookmark.objects.create(user=user, name="Test")
        Bookmark.objects.create(user=user, name="Test", list=list1)
        Bookmark.objects.create(user=user, name="Test", list=list2)

        user.delete()

        self.assertFalse(List.objects.all().exists())
        self.assertFalse(Bookmark.objects.all().exists())

    def test_list_delete(self):
        user = User.objects.create_user("test@example.com", "12345")
        list1 = List.objects.create(user=user, name="Test")
        bookmark1 = Bookmark.objects.create(user=user, name="Test", list=list1)

        list1.delete()

        self.assertTrue(Bookmark.objects.filter(pk=bookmark1.pk).exists())

    def test_delete_related(self):
        user = User.objects.create_user("test@example.com", "12345")
        list1 = List.objects.create(user=user, name="Test")
        bookmark1 = Bookmark.objects.create(user=user, name="Test", list=list1)

        list1.delete_related_bookmarks()

        self.assertFalse(Bookmark.objects.filter(pk=bookmark1.pk).exists())
