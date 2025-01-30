from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import (
    LoginView as CoreLoginView,
)
from django.contrib.auth.views import (
    LogoutView as CoreLogoutView,
)
from django.views.generic import TemplateView

from core.views import (
    BaseAdminCreateView,
    BaseAdminDeleteView,
    BaseAdminListView,
    BaseAdminUpdateView,
)

from .forms import CreateUserForm, EditUserForm, GroupForm
from .models import User
from property.models import Property


class AdminLoginView(CoreLoginView):
    form_class = AuthenticationForm
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


class CustomerProfileView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/profile.html"


class CustomerHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/history.html"


class CustomerReviewView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/reviews.html"


class CustomerListingView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/customer/listing.html"
