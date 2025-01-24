from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from accounts.models import User
from property.models import Property, PropertyType

from .forms import (
    AboutUsForm,
    ContactInfoForm,
    FAQForm,
    PrivacyPolicyForm,
    SiteBasicForm,
    SiteFooterForm,
    SiteLinksForm,
    SiteSettingsForm,
    TermsAndConditionForm,
)
from .models import (
    FAQ,
    AboutUs,
    ContactInfo,
    ContactUs,
    PrivacyPolicy,
    SiteSettings,
    TermsAndCondition,
)


class AdminLoginRequired(LoginRequiredMixin):
    login_url = "/admin/login/"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BaseAdminCreateView(AdminLoginRequired, CreateView):
    pass


class BaseAdminListView(AdminLoginRequired, ListView):
    pass


class BaseAdminUpdateView(AdminLoginRequired, UpdateView):
    pass


class BaseAdminDeleteView(AdminLoginRequired, DeleteView):
    pass


class DashboardView(AdminLoginRequired, TemplateView):
    template_name = "admin/pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_count"] = User.objects.count()
        context["property_count"] = Property.objects.count()
        context["type_count"] = PropertyType.objects.count()
        latest_properties = Property.objects.order_by("-created_at")[:5]
        viewed_properties = Property.objects.order_by("-views")[:5]
        popular_properties = Property.objects.filter(is_popular=True)[:5]

        context.update(
            {
                "latest_properties": latest_properties,
                "viewed_properties": viewed_properties,
                "popular_properties": popular_properties,
            }
        )

        current_month = datetime.now().month
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

        context["months"] = months[:current_month]

        monthly_user_counts = (
            User.objects.filter(date_joined__year=datetime.now().year)
            .values("date_joined__month")
            .annotate(count=Count("id"))
        )
        user_counts = {
            entry["date_joined__month"]: entry["count"] for entry in monthly_user_counts
        }

        context["users"] = [
            user_counts.get(month, 0) for month in range(1, current_month + 1)
        ]

        return context


class SiteSettingView(AdminLoginRequired, FormView):
    template_name = "admin/pages/settings.html"
    success_url = "/admin/settings/"

    form_mapping = {
        "site_settings": {
            "form_class": SiteSettingsForm,
            "model": SiteSettings,
        },
        "footer": {
            "form_class": SiteFooterForm,
            "model": SiteSettings,
        },
        "links": {
            "form_class": SiteLinksForm,
            "model": SiteSettings,
        },
        "basic": {
            "form_class": SiteBasicForm,
            "model": SiteSettings,
        },
        "contact_info": {
            "form_class": ContactInfoForm,
            "model": ContactInfo,
        },
        "about_us": {
            "form_class": AboutUsForm,
            "model": AboutUs,
        },
        "terms_and_condition": {
            "form_class": TermsAndConditionForm,
            "model": TermsAndCondition,
        },
        "privacy_policy": {
            "form_class": PrivacyPolicyForm,
            "model": PrivacyPolicy,
        },
    }

    def get_form_class(self):
        form_type = self.request.POST.get("form_type", "site_settings")
        form_info = self.form_mapping.get(form_type)
        if form_info:
            return form_info["form_class"]
        return SiteSettingsForm

    def form_valid(self, form):
        form_type = self.request.POST.get("form_type", "site_settings")
        form_info = self.form_mapping.get(form_type)
        if not form_info:
            return redirect(self.success_url)

        model_class = form_info["model"]
        instance = model_class.load()

        for field, value in form.cleaned_data.items():
            if field in self.request.FILES:
                setattr(instance, field, self.request.FILES[field])
            else:
                setattr(instance, field, value)
        instance.save()

        messages.success(self.request, "Details saved")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.load()
        context["contact_info"] = ContactInfo.load()
        context["about_us"] = AboutUs.load()
        context["terms_and_condition"] = TermsAndCondition.load()
        context["privacy_policy"] = PrivacyPolicy.load()

        return context

    def form_invalid(self, form):
        form_type = self.request.POST.get("form_type", "site_settings")
        context = self.get_context_data()
        print(form_type)
        context["form_type_with_errors"] = form_type
        context["form"] = form
        return self.render_to_response(context)


class ContactUsListView(BaseAdminListView):
    model = ContactUs
    template_name = "admin/pages/contact_us.html"


class ContactUsDeleteView(BaseAdminDeleteView):
    model = ContactUs
    template_name = "admin/pages/contact_us.html"
    success_url = "/admin/contact_us/"


class FAQListView(BaseAdminListView):
    model = FAQ
    template_name = "admin/pages/faq/index.html"


class FAQCreateView(BaseAdminCreateView):
    model = FAQ
    form_class = FAQForm
    template_name = "admin/pages/faq/create.html"
    success_url = "/admin/faq/"


class FAQUpdateView(BaseAdminUpdateView):
    model = FAQ
    form_class = FAQForm
    template_name = "admin/pages/faq/edit.html"
    success_url = "/admin/faq/"


class FAQDeleteView(BaseAdminDeleteView):
    model = FAQ
    template_name = "admin/pages/faq/index.html"
    success_url = "/admin/faq/"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/home.html"


class AboutUsView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/about_us.html"


class ContactUsView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/contact_us.html"


class TermsAndConditionView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/terms_and_condition.html"


class PrivacyPolicyView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/privacy_policy.html"


class FAQView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/faq.html"
