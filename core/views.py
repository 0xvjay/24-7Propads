from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Value
from django.db.models.functions import Coalesce, TruncMonth
from django.db.models.functions import Lower as LowerCase
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
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
    ContactUsForm,
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
from .utils import get_date_range


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

        context["latest_properties"] = Property.objects.order_by("-created_at")[:5]
        context["viewed_properties"] = Property.objects.annotate(
            view_count=Count("browsing_stats")
        ).order_by("-view_count")[:5]
        context["popular_properties"] = Property.objects.order_by("-rating")[:5]

        start_date, end_date = get_date_range()
        qs = (
            User.objects.filter(
                date_joined__date__gte=start_date, date_joined__date__lte=end_date
            )
            .annotate(month=TruncMonth("date_joined"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        month_data = {entry["month"].strftime("%B"): entry["count"] for entry in qs}
        month_list, user_counts = [], []
        current = start_date
        while current <= end_date:
            month_name = current.strftime("%B")
            month_list.append(month_name)
            user_counts.append(month_data.get(month_name, 0))
            current += relativedelta(months=1)

        context.update({"months": month_list, "users": user_counts})
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


class HomeView(TemplateView):
    template_name = "customer/pages/home.html"

    def get_context_data(self, **kwargs):
        cities = ["ahmedabad", "mumbai", "delhi", "bangalore", "kolkata"]

        context = super().get_context_data(**kwargs)
        property_counts = PropertyType.objects.annotate(
            property_count=Count("properties")
        ).values("name", "property_count")

        context.update(
            {
                property_type["name"]
                .lower()
                .replace("/", "_")
                .replace(" ", "_"): property_type["property_count"]
                for property_type in property_counts
            }
        )
        context["about_us"] = AboutUs.load()
        context["featured_properties"] = Property.objects.all()[:3]
        context.update({f"{city.lower()}_count": 0 for city in cities})
        for city, count in (
            Property.objects.annotate(lower_city=LowerCase("city"))
            .filter(lower_city__in=cities)
            .values("city")
            .annotate(count=Coalesce(Count("id"), Value(0)))
            .values_list("city", "count")
        ):
            context[f"{city.lower()}_count"] = count

        return context


class AboutUsView(DetailView):
    model = AboutUs
    template_name = "customer/pages/about_us.html"

    def get_object(self, *args, **kwargs):
        return AboutUs.load()


class ContactUsView(CreateView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = "customer/pages/contact_us.html"
    success_url = "/contact_us/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = ContactInfo.load()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Message sent successfully")
        return super().form_valid(form)


class TermsAndConditionView(DetailView):
    model = TermsAndCondition
    template_name = "customer/pages/terms_and_condition.html"

    def get_object(self, *args, **kwargs):
        return TermsAndCondition.load()


class PrivacyPolicyView(DetailView):
    model = PrivacyPolicy
    template_name = "customer/pages/privacy_policy.html"

    def get_object(self, *args, **kwargs):
        return PrivacyPolicy.load()


class FAQView(TemplateView):
    template_name = "customer/pages/faq.html"
