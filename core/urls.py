from django.urls import path

from .views import (
    ContactUsDeleteView,
    ContactUsListView,
    DashboardView,
    FAQCreateView,
    FAQDeleteView,
    FAQListView,
    FAQUpdateView,
    SiteSettingView,
    HomeView,
    AboutUsView,
    ContactUsView,
    TermsAndConditionView,
    PrivacyPolicyView,
    FAQView,
)

app_name = "core"
urlpatterns = [
    path(r"admin/", DashboardView.as_view(), name="dashboard"),
    path(r"admin/settings/", SiteSettingView.as_view(), name="site_settings"),
    # contact_us
    path(r"admin/contact_us/", ContactUsListView.as_view(), name="admin_contact_us"),
    path(
        r"admin/contact_us/delete/<int:pk>/",
        ContactUsDeleteView.as_view(),
        name="delete_contact_us",
    ),
    # faq
    path(r"admin/faq/", FAQListView.as_view(), name="admin_faq"),
    path(r"admin/faq/add", FAQCreateView.as_view(), name="add_faq"),
    path(r"admin/faq/edit/<int:pk>/", FAQUpdateView.as_view(), name="edit_faq"),
    path(r"admin/faq/delete/<int:pk>/", FAQDeleteView.as_view(), name="delete_faq"),
    # customer urls
    path(r"", HomeView.as_view(), name="home"),
    path(r"about_us/", AboutUsView.as_view(), name="about_us"),
    path(r"contact_us/", ContactUsView.as_view(), name="contact_us"),
    path(
        r"terms_and_conditions/",
        TermsAndConditionView.as_view(),
        name="terms_and_conditions",
    ),
    path(r"privacy_policy/", PrivacyPolicyView.as_view(), name="privacy_policy"),
    path(r"faq/", FAQView.as_view(), name="faq"),
]
