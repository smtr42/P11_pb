from django.test import TestCase
from django.urls import reverse

from products.models import Category, Favorite, Product
from users.models import User


class HomePageViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("pages:index"))
        self.assertEqual(response.status_code, 200)


class NoticePageViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse("pages:notice"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("pages:notice"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/notice.html")


class UserLoginViewTest(TestCase):
    def test_login_view_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")


class UserSignupViewTest(TestCase):
    def test_signup_view_url_exists(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")
