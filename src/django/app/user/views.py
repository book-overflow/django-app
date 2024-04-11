from .forms import CustomUserCreationForm
from .decorators import guest_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from .tokens import account_activation_token
from student_profile.decorators import profile_required


# Add guest_required decorator to built-in LoginView
class CustomLoginView(LoginView):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return guest_required(view)


# Require users to be logged in/authenticated to access built-in LogoutView
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("user-login")
        return super().get(request, *args, **kwargs)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("user-register-profile")
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect("register")


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "activate_account.html",
        {
            "user": user.first_name,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            mark_safe(
                f"Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder."
            ),
        )
    else:
        messages.error(
            request,
            f"Problem sending email to {to_email}, check if you typed it correctly.",
        )


@guest_required
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            activateEmail(request, user, form.cleaned_data.get("email"))
            # Authenticate the user
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            if user is not None and user.is_active:
                # Log the user in
                login(request, user)
                request.session["name"] = form.cleaned_data["first_name"]
                return redirect("create-profile")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "register.html", context)


@login_required
@profile_required
def browse(request):
    return render(request, "browse.html")
