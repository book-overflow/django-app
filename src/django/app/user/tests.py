from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from .views import CustomLoginView, CustomLogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .views import CustomLoginView, CustomLogoutView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.core import mail

User = get_user_model()


class CustomLoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="john@nyu.edu", password="password123"
        )

    def test_guest_required_decorator(self):
        # User is logged in
        request = self.factory.get(reverse("login"))
        request.user = self.user

        response = CustomLoginView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Expecting redirect
        self.assertTrue(
            "/" in response.url
        )  # Redirect to homepage or defined redirect URL

        # User is not logged in
        request.user = AnonymousUser()
        response = CustomLoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)  # Should allow to view the page


class CustomLogoutViewTests(TestCase):
    def test_logout_redirect_if_not_authenticated(self):
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("user-login"))


from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token


class ActivationTests(TestCase):
    def test_activate_user(self):
        user = User.objects.create_user(
            email="jane@nyu.edu",
            password="password123",
            is_active=False,
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        response = self.client.get(
            reverse("activate", kwargs={"uidb64": uid, "token": token})
        )
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertRedirects(response, reverse("create-profile"))


from django.core import mail


# class ActivateEmailTests(TestCase):
#     def test_send_activation_email(self):
#         user = User.objects.create_user(
#             username="jane", email="jane@example.com", password="secret"
#         )
#         request = self.factory.post(reverse("register"), {"email": "jane@example.com"})
#         request.user = AnonymousUser()

#         activateEmail(request, user, "jane@example.com")
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].subject, "Activate your user account.")


class RegisterTests(TestCase):
    def test_register_form(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "complexpassword",
                "password2": "complexpassword",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Assuming redirect to an intermediate page
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(mail.outbox[0].subject, "Activate your user account.")
