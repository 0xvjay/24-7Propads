from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import (
    LoginView as CoreLoginView,
)
from django.contrib.auth.views import (
    LogoutView as CoreLogoutView,
)
from django.contrib.auth.views import (
    PasswordChangeView as CorePasswordChangeView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as CorePasswordResetConfirmView,
)
from django.contrib.auth.views import (
    PasswordResetView as CorePasswordResetView,
)
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from core.views import (
    BaseAdminCreateView,
    BaseAdminDeleteView,
    BaseAdminListView,
    BaseAdminUpdateView,
)
from property.models import Property

from .forms import CreateUserForm, EditUserForm, GroupForm, RegisterUserForm
from .models import User


class AdminLoginView(CoreLoginView):
    template_name = "admin/admin_login.html"

    def get_success_url(self):
        return "/admin/"


class AdminLogoutView(CoreLogoutView):
    template_name = "admin/admin_logout.html"


class UserListView(BaseAdminListView):
    model = User
    template_name = "admin/pages/user/index.html"


class UserCreateView(BaseAdminCreateView):
    model = User
    form_class = CreateUserForm
    template_name = "admin/pages/user/create.html"
    success_url = "/admin/users/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        return context


class UserUpdateView(BaseAdminUpdateView):
    model = User
    form_class = EditUserForm
    template_name = "admin/pages/user/edit.html"
    success_url = "/admin/users/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        return context


class UserDeleteView(BaseAdminDeleteView):
    model = User
    template_name = "admin/pages/user/index.html"
    success_url = "/admin/users/"


class GroupListView(BaseAdminListView):
    model = Group
    template_name = "admin/pages/group/index.html"


class GroupCreateView(BaseAdminCreateView):
    model = Group
    form_class = GroupForm
    template_name = "admin/pages/group/create.html"
    success_url = "/admin/groups/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permissions"] = Permission.objects.all()
        return context


class GroupUpdateView(BaseAdminUpdateView):
    model = Group
    form_class = GroupForm
    template_name = "admin/pages/group/edit.html"
    success_url = "/admin/groups/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permissions"] = Permission.objects.all()
        return context


class GroupDeleteView(BaseAdminDeleteView):
    model = Group
    template_name = "admin/pages/group/index.html"
    success_url = "/admin/groups/"


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_listings"] = Property.objects.filter(
            user=self.request.user
        ).count()
        return context


class CustomerProfileView(LoginRequiredMixin, FormView):
    template_name = "customer/pages/customer/profile.html"
    form_class = EditUserForm


class CustomerHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/history.html"


class CustomerReviewView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/reviews.html"


class CustomerListingView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/listing.html"


class CustomerLoginView(CoreLoginView):
    template_name = "customer/pages/home.html"

    def form_valid(self, form):
        messages.success(self.request, f"Welcome, {self.request.user.get_full_name()}!")
        return super().form_valid(form)


class CustomerLogoutView(CoreLogoutView):
    template_name = "customer/pages/home.html"

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect("/")


class CustomerRegisterView(FormView):
    form_class = RegisterUserForm
    template_name = "customer/pages/home.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "User created successfully")
        return super().form_valid(form)


class ChangePasswordView(CorePasswordChangeView):
    template_name = "customer/pages/customer/profile.html"
    success_url = "/accounts/profile/"

    def form_valid(self, form):
        messages.success(self.request, "Password Changed successfully")
        return super().form_valid(form)


class PasswordResetView(CorePasswordResetView):
    template_name = "customer/base.html"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Email sent successfully")
        return super().form_valid(form)


class PasswordResetConfirmView(CorePasswordResetConfirmView):
    template_name = "customer/pages/password-reset.html"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Password changed")
        return super().form_valid(form)
