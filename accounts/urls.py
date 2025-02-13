from django.urls import path

from .views import (
    AdminLoginView,
    AdminLogoutView,
    ChangePasswordView,
    CustomerDashboardView,
    CustomerHistoryView,
    CustomerListingView,
    CustomerLoginView,
    CustomerLogoutView,
    CustomerProfileView,
    CustomerRegisterView,
    CustomerReviewView,
    GroupCreateView,
    GroupDeleteView,
    GroupListView,
    GroupUpdateView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

app_name = "accounts"
urlpatterns = [
    path(r"admin/login/", AdminLoginView.as_view(), name="admin_login"),
    path(r"admin/logout/", AdminLogoutView.as_view(), name="admin_logout"),
    # users
    path(r"admin/users/", UserListView.as_view(), name="users"),
    path(r"admin/users/add", UserCreateView.as_view(), name="add_user"),
    path(r"admin/users/edit/<int:pk>/", UserUpdateView.as_view(), name="edit_user"),
    path(r"admin/users/delete/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
    # groups
    path(r"admin/groups/", GroupListView.as_view(), name="groups"),
    path(r"admin/groups/add", GroupCreateView.as_view(), name="add_group"),
    path(r"admin/groups/edit/<int:pk>/", GroupUpdateView.as_view(), name="edit_group"),
    path(
        r"admin/groups/delete/<int:pk>/", GroupDeleteView.as_view(), name="delete_group"
    ),
    # customer
    path(r"logout/", CustomerLogoutView.as_view(), name="logout"),
    path(r"password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        r"password_reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(r"accounts/", CustomerDashboardView.as_view(), name="dashboard"),
    path(
        r"accounts/change-password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(r"accounts/register/", CustomerRegisterView.as_view(), name="register"),
    path(r"accounts/login/", CustomerLoginView.as_view(), name="login"),
    path(r"accounts/history/", CustomerHistoryView.as_view(), name="history"),
    path(r"accounts/reviews/", CustomerReviewView.as_view(), name="reviews"),
    path(r"accounts/listing/", CustomerListingView.as_view(), name="listing"),
    path(r"accounts/profile/", CustomerProfileView.as_view(), name="profile"),
]
