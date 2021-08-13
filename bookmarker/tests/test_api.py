import json
import re
from django.contrib.auth import get_user
from django.core import mail
from django.test.testcases import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from bookmarker.models import Bookmark, List, User


class CreateModifyDeleteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test1@example.com", password="12345", is_confirmed=True
        )
        self.user2 = User.objects.create_user(
            email="test2@example.com", password="12345", is_confirmed=True
        )
        self.client.force_login(self.user)

    def test_bookmark_create(self):
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark2", "url": "http://example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        query = Bookmark.objects.filter(user=self.user)
        self.assertTrue(query.filter(name="Bookmark1").exists())
        self.assertTrue(query.filter(name="Bookmark2").exists())

    def test_bookmark_modify(self):
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com"},
            format="json",
        )
        bookmark_1 = response.data["id"]
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark2", "url": "http://example.com"},
            format="json",
        )
        bookmark_2 = response.data["id"]

        response = self.client.patch(
            f"/api/bookmarks/{bookmark_1}/", {"name": "Bookmark3"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(
            f"/api/bookmarks/{bookmark_2}/", {"name": "Bookmark4"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        query = Bookmark.objects.filter(user=self.user)
        self.assertFalse(query.filter(name="Bookmark1").exists())
        self.assertTrue(query.filter(name="Bookmark3").exists())
        self.assertFalse(query.filter(name="Bookmark2").exists())
        self.assertTrue(query.filter(name="Bookmark4").exists())

        self.client.force_login(self.user2)
        response = self.client.patch(
            f"/api/bookmarks/{bookmark_1}/", {"name": "Bad Bookmark"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(query.get(id=bookmark_1).name, "Bad Bookmark")

    def test_list_create(self):
        response = self.client.post(
            "/api/lists/", {"name": "List1", "url": "http://example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            "/api/lists/", {"name": "List2", "url": "http://example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        query = List.objects.filter(user=self.user)
        self.assertTrue(query.filter(name="List1").exists())
        self.assertTrue(query.filter(name="List2").exists())

    def test_list_modify(self):
        response = self.client.post("/api/lists/", {"name": "List1"}, format="json")
        list_1 = response.data["id"]
        response = self.client.post("/api/lists/", {"name": "List2"}, format="json")
        list_2 = response.data["id"]

        response = self.client.patch(
            f"/api/lists/{list_1}/", {"name": "List3"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(
            f"/api/lists/{list_2}/", {"name": "List4"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        query = List.objects.filter(user=self.user)
        self.assertFalse(query.filter(name="List1").exists())
        self.assertTrue(query.filter(name="List3").exists())
        self.assertFalse(query.filter(name="List2").exists())
        self.assertTrue(query.filter(name="List4").exists())

        self.client.force_login(self.user2)
        response = self.client.patch(f"/api/lists/{list_1}/", {"name": "Bad List"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(query.get(id=list_1).name, "Bad List")

    def test_list_delete_keep_bookmarks(self):
        response = self.client.post("/api/lists/", {"name": "List1"}, format="json")
        list_id = response.data["id"]
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com", "list": list_id},
            format="json",
        )
        bookmark_id = response.data["id"]

        response = self.client.delete(f"/api/lists/{list_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(List.objects.filter(id=list_id).exists())
        bookmark = Bookmark.objects.filter(id=bookmark_id).first()
        self.assertIsNotNone(bookmark)
        self.assertIsNone(bookmark.list)

    def test_list_delete_and_related_bookmarks(self):
        response = self.client.post("/api/lists/", {"name": "List1"}, format="json")
        list_id = response.data["id"]
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com", "list": list_id},
            format="json",
        )
        bookmark_id = response.data["id"]

        response = self.client.delete(f"/api/lists/{list_id}/include-related/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(List.objects.filter(id=list_id).exists())
        self.assertFalse(Bookmark.objects.filter(id=bookmark_id).exists())


class GetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test1@example.com", password="12345", is_confirmed=True
        )
        self.user2 = User.objects.create_user(
            email="test2@example.com", password="12345", is_confirmed=True
        )
        self.client.force_login(self.user)

    def test_get_single_bookmark(self):
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com"},
            format="json",
        )
        bookmark_id = response.data["id"]

        response = self.client.get(f"/api/bookmarks/{bookmark_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": bookmark_id,
                "unread": True,
                "list": None,
                "name": "Bookmark1",
                "url": "http://example.com",
            },
        )

        self.client.force_login(self.user2)
        response = self.client.get(f"/api/bookmarks/{bookmark_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_bookmarks(self):
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com"},
            format="json",
        )
        bookmark1_id = response.data["id"]
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark2", "url": "http://example.com"},
            format="json",
        )
        bookmark2_id = response.data["id"]

        response = self.client.get("/api/bookmarks/", format="json")
        self.assertIn(
            {
                "id": bookmark1_id,
                "unread": True,
                "list": None,
                "name": "Bookmark1",
                "url": "http://example.com",
            },
            response.data,
        )
        self.assertIn(
            {
                "id": bookmark2_id,
                "unread": True,
                "list": None,
                "name": "Bookmark2",
                "url": "http://example.com",
            },
            response.data,
        )

        self.client.force_login(self.user2)
        response = self.client.get("/api/bookmarks/", format="json")
        self.assertNotIn(
            {
                "id": bookmark1_id,
                "unread": True,
                "list": None,
                "name": "Bookmark1",
                "url": "http://example.com",
            },
            response.data,
        )
        self.assertNotIn(
            {
                "id": bookmark2_id,
                "unread": True,
                "list": None,
                "name": "Bookmark2",
                "url": "http://example.com",
            },
            response.data,
        )

    def test_get_single_list(self):
        response = self.client.post("/api/lists/", {"name": "List1"}, format="json")
        list_id = response.data["id"]

        response = self.client.get(f"/api/lists/{list_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": list_id, "name": "List1"})

        self.client.force_login(self.user2)
        response = self.client.get(f"/api/lists/{list_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_lists(self):
        response = self.client.post("/api/lists/", {"name": "List1"}, format="json")
        list1_id = response.data["id"]
        response = self.client.post("/api/lists/", {"name": "List2"}, format="json")
        list2_id = response.data["id"]

        response = self.client.get("/api/lists/", format="json")
        self.assertIn({"id": list1_id, "name": "List1"}, response.data)
        self.assertIn({"id": list2_id, "name": "List2"}, response.data)

        self.client.force_login(self.user2)
        response = self.client.get("/api/lists/", format="json")
        self.assertNotIn({"id": list1_id, "name": "List1"}, response.data)
        self.assertNotIn({"id": list2_id, "name": "List2"}, response.data)

    def test_get_bookmarks_filtered_by_list(self):
        list1 = List.objects.create(name="List1", user=self.user)
        Bookmark.objects.create(
            name="Bookmark1", url="http://example.com", user=self.user, list=list1
        )
        Bookmark.objects.create(
            name="Bookmark2", url="http://example.com", user=self.user
        )

        response = self.client.get(f"/api/bookmarks/?list={list1.id}")

        self.assertContains(response, "Bookmark1")
        self.assertNotContains(response, "Bookmark2")

        self.client.force_login(self.user2)
        response = self.client.get(f"/api/bookmarks/?list={list1.id}")

        self.assertNotContains(response, "Bookmark1")
        self.assertNotContains(response, "Bookmark2")

    def test_get_bookmarks_filtered_by_unread(self):
        Bookmark.objects.create(
            name="Bookmark1", url="http://example.com", user=self.user
        )
        Bookmark.objects.create(
            name="Bookmark2", url="http://example.com", user=self.user, unread=False
        )

        response = self.client.get("/api/bookmarks/?unread=true")

        self.assertContains(response, "Bookmark1")
        self.assertNotContains(response, "Bookmark2")

        response = self.client.get("/api/bookmarks/?unread=false")

        self.assertNotContains(response, "Bookmark1")
        self.assertContains(response, "Bookmark2")

        self.client.force_login(self.user2)
        response = self.client.get("/api/bookmarks/?unread=1")

        self.assertNotContains(response, "Bookmark1")
        self.assertNotContains(response, "Bookmark2")

        response = self.client.get("/api/bookmarks/?unread=0")

        self.assertNotContains(response, "Bookmark1")
        self.assertNotContains(response, "Bookmark2")

    def test_get_bookmarks_ordered_by_name(self):
        Bookmark.objects.create(
            name="Bookmark1", url="http://example.com", user=self.user
        )
        Bookmark.objects.create(
            name="Bookmark2", url="http://example.com", user=self.user
        )

        response = self.client.get("/api/bookmarks/?ordering=name")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Bookmark1")
        self.assertEqual(response.data[1]["name"], "Bookmark2")

        response = self.client.get("/api/bookmarks/?ordering=-name")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Bookmark2")
        self.assertEqual(response.data[1]["name"], "Bookmark1")

    def test_get_bookmarks_ordered_by_url(self):
        bookmark1 = Bookmark.objects.create(
            name="Bookmark", url="http://example.com/a/", user=self.user
        )
        bookmark2 = Bookmark.objects.create(
            name="Bookmark", url="http://example.com/b/", user=self.user
        )

        response = self.client.get("/api/bookmarks/?ordering=url")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], bookmark1.id)
        self.assertEqual(response.data[1]["id"], bookmark2.id)

        response = self.client.get("/api/bookmarks/?ordering=-url")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], bookmark2.id)
        self.assertEqual(response.data[1]["id"], bookmark1.id)

    def test_get_lists_ordered_by_name(self):
        List.objects.create(name="List1", user=self.user)
        List.objects.create(name="List2", user=self.user)

        response = self.client.get("/api/lists/?ordering=name")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "List1")
        self.assertEqual(response.data[1]["name"], "List2")

        response = self.client.get("/api/lists/?ordering=-name")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "List2")
        self.assertEqual(response.data[1]["name"], "List1")

    def test_get_bookmarks_by_search(self):
        Bookmark.objects.create(
            name="Bookmark1", url="http://example.com/a/", user=self.user
        )
        Bookmark.objects.create(
            name="Bookmark2", url="http://example.com/b/", user=self.user
        )

        response = self.client.get("/api/bookmarks/?search=1")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Bookmark1")

        response = self.client.get("/api/bookmarks/?search=2")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Bookmark2")

        response = self.client.get("/api/bookmarks/?search=%2Fa%2F")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Bookmark1")

        response = self.client.get("/api/bookmarks/?search=%2Fb%2F")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Bookmark2")


class DifferentUsersLists(APITestCase):
    def test_lists_of_different_users(self):
        """
        Tests to verify that a bookmark associated with one user cannot become part of
        a list of another user.
        """
        user = User.objects.create_user(
            email="test1@example.com", password="12345", is_confirmed=True
        )
        user2 = User.objects.create_user(
            email="test2@example.com", password="12345", is_confirmed=True
        )
        list1_id = List.objects.create(name="List1", user=user).id
        list2_id = List.objects.create(name="List2", user=user2).id

        self.client.force_login(user2)
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com", "list": list1_id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com", "list": list2_id},
            format="json",
        )
        bookmark_id = response.data["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.patch(
            f"/api/bookmarks/{bookmark_id}/",
            {"id": bookmark_id, "list": list1_id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ForbiddenRequestsTests(APITestCase):
    """
    This tests that the API will return HTTP 403 when user is not logged in.
    """

    def test_request_nothing_exists_get(self):
        """
        Tests for HTTP 403 when there are no bookmarks or lists.
        """
        response = self.client.get("/api/bookmarks/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get("/api/bookmarks/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get("/api/lists/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get("/api/lists/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_get_existing(self):
        """
        Tests for HTTP 403 when there are bookmarks or lists.
        """
        user = User.objects.create_user(
            email="test1@example.com", password="12345", is_confirmed=True
        )
        bookmark_id = Bookmark.objects.create(
            name="Bookmark1", url="http://example.com", user=user
        ).id
        list_id = List.objects.create(name="List1", user=user).id

        response = self.client.get("/api/bookmarks/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(f"/api/bookmarks/{bookmark_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get("/api/lists/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(f"/api/lists/{list_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_create(self):
        """
        Tests for HTTP 403 when trying to create bookmarks or lists.
        """
        response = self.client.post(
            "/api/bookmarks/",
            {"name": "Bookmark1", "url": "http://example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(
            "/api/lists/", {"name": "List1", "url": "http://example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_modify_existing(self):
        """
        Tests for HTTP 403 when trying to modify existing bookmarks or lists.
        """
        user = User.objects.create_user(
            email="test1@example.com", password="12345", is_confirmed=True
        )
        bookmark_id = Bookmark.objects.create(
            name="Bookmark1", url="http://example.com", user=user
        ).id
        list_id = List.objects.create(name="List1", user=user).id

        response = self.client.patch(
            f"/api/bookmarks/{bookmark_id}/", {"name": "Bookmark2"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            f"/api/lists/{list_id}/", {"name": "List2"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            f"/api/bookmarks/{bookmark_id}/", {"list": list_id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserInfoTests(APITestCase):
    def test_get_user_info(self):
        user = User.objects.create_user(email="test@example.com", password="12345")
        self.client.force_login(user)

        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": user.id, "email": "test@example.com", "is_confirmed": False},
        )

    def test_bad_get_user_info(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserManagementTests(TestCase):
    def setUp(self):
        self.client.get("/api/set-cookie/")

    def test_login(self):
        User.objects.create_user(email="test@example.com", password="12345")
        response = self.client.post(
            "/api/login/",
            {"email": "test@example.com", "password": "12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_bad_login(self):
        User.objects.create_user(email="test@example.com", password="12345")
        response = self.client.post(
            "/api/login/",
            {"email": "test@example.com", "password": "67890"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            "/api/login/",
            {"email": "nothing@example.com", "password": "12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register(self):
        response = self.client.post(
            "/api/register/",
            {"email": "test@example.com", "password": "12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        message_body = mail.outbox[0].body

        regex = r"/confirm/(\d+)/([A-Za-z\d]+)/"
        match = re.search(regex, message_body)
        user_id, token_str = match.groups()
        response = self.client.get(f"/confirm/{user_id}/{token_str}/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.headers["Location"], "/confirmed/")
        user = User.objects.get(id=user_id)
        self.assertTrue(user.is_confirmed)

    def test_bad_register_preexisting_email(self):
        User.objects.create(email="test@example.com", password="12345")

        response = self.client.post(
            "/api/register/",
            {"email": "test@example.com", "password": "12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "An account with this email already exists", str(response.content)
        )

    def test_bad_confirmation(self):
        response = self.client.post(
            "/api/register/",
            {"email": "test@example.com", "password": "12345"},
            format="json",
        )
        user = User.objects.first()
        token = user.email_confirm_token

        response = self.client.get(f"/confirm/{user.id}/12345/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f"/confirm/12345/{token}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f"/confirm/{user.id}/{token}/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.headers["Location"], "/confirmed/")

    def test_resend_confirmation(self):
        response = self.client.post(
            "/api/register/",
            {"email": "test@example.com", "password": "12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        message1_body = mail.outbox[0].body

        response = self.client.post("/api/resend-confirmation/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 2)
        message2_body = mail.outbox[1].body
        self.assertEqual(message1_body, message2_body)

    def test_bad_resend_confirmation(self):
        response = self.client.post("/api/resend-confirmation/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 0)

    def test_logout(self):
        user = User.objects.create_user(email="test@example.com", password="12345")
        self.client.force_login(user)

        response = self.client.post("/api/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        potential_user = get_user(self.client)
        self.assertFalse(potential_user.is_authenticated)

    def test_get_confirmed_status(self):
        user = User.objects.create_user(email="test@example.com", password="12345")
        self.client.force_login(user)

        response = self.client.get("/api/confirmed-status/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"detail": False})

        user.is_confirmed = True
        user.save()

        response = self.client.get("/api/confirmed-status/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"detail": True})

    def test_bad_get_confirmed_status(self):
        response = self.client.get("/api/confirmed-status/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
