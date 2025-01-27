from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import DefaultStorage
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from core.views import (
    BaseAdminCreateView,
    BaseAdminDeleteView,
    BaseAdminListView,
    BaseAdminUpdateView,
)

from .forms import (
    AgricultureLandForm,
    FlatForm,
    HouseForm,
    OfficeForm,
    PlotForm,
    PropertyForm,
    TypeForm,
    VillaForm,
)
from .models import Property, PropertyAttributes, PropertyType


class TypeListView(BaseAdminListView):
    model = PropertyType
    template_name = "admin/pages/type/index.html"


class TypeCreateView(BaseAdminCreateView):
    model = PropertyType
    template_name = "admin/pages/type/create.html"
    form_class = TypeForm
    success_url = "/admin/types/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attributes"] = PropertyAttributes.objects.all()
        return context


class TypeUpdateView(BaseAdminUpdateView):
    model = PropertyType
    template_name = "admin/pages/type/edit.html"
    form_class = TypeForm
    success_url = "/admin/types/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attributes"] = PropertyAttributes.objects.all()
        return context


class TypeDeleteView(BaseAdminDeleteView):
    model = PropertyType
    template_name = "admin/pages/type/index.html"
    success_url = "/admin/types/"


class PropertyListView(BaseAdminListView):
    model = Property
    template_name = "admin/pages/property/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = PropertyType.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        filter_conditions = Q()

        category = self.request.GET.get("category")
        if category:
            filter_conditions &= {
                "enable": Q(is_active=True),
                "disable": Q(is_active=False),
                "featured": Q(is_featured=True),
                "no_featured": Q(is_featured=False),
            }.get(category, Q())

        post_type = self.request.GET.get("post_type")
        if post_type:
            filter_conditions &= Q(post_type=post_type)

        type_name = self.request.GET.get("type")
        if type_name:
            filter_conditions &= Q(type__name=type_name)

        queryset = queryset.filter(filter_conditions)
        return queryset


def show_agriculture_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0") or {}
    type_data = cleaned_data.get("type")
    if type_data and type_data.name == "Agriculture Land":
        return True
    return False


def show_villa_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0") or {}
    type_data = cleaned_data.get("type")
    if type_data and type_data.name == "Villa/Independent House":
        return True
    return False


def show_house_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0") or {}
    type_data = cleaned_data.get("type")
    if type_data and type_data.name == "House":
        return True
    return False


def show_flat_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0") or {}
    type_data = cleaned_data.get("type")
    if type_data and type_data.name == "Flat/Apartment":
        return True
    return False


def show_office_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0") or {}
    type_data = cleaned_data.get("type")
    if type_data and type_data.name == "Office/Commercial Space":
        return True
    return False


def show_plot_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0") or {}
    type_data = cleaned_data.get("type")
    if type_data and type_data.name == "Open Plot":
        return True
    return False


TEMPLATES = {
    "0": "admin/pages/property/create/property.html",
    "1": "admin/pages/property/create/agriculture.html",
    "2": "admin/pages/property/create/villa.html",
    "3": "admin/pages/property/create/house.html",
    "4": "admin/pages/property/create/flat.html",
    "5": "admin/pages/property/create/office.html",
    "6": "admin/pages/property/create/plot.html",
}

FORMS = [
    ("0", PropertyForm),
    ("1", AgricultureLandForm),
    ("2", VillaForm),
    ("3", HouseForm),
    ("4", FlatForm),
    ("5", OfficeForm),
    ("6", PlotForm),
]
CONDITION_DICT = {
    "1": show_agriculture_form,
    "2": show_villa_form,
    "3": show_house_form,
    "4": show_flat_form,
    "5": show_office_form,
    "6": show_plot_form,
}


class PropertyCreateView(SessionWizardView):
    file_storage = DefaultStorage()
    form_list = FORMS
    condition_dict = CONDITION_DICT

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return redirect("/admin/")


class PropertyUpdateView(SessionWizardView):
    file_storage = DefaultStorage()
    form_list = FORMS
    condition_dict = CONDITION_DICT

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return redirect("/admin/")


class PropertyDeleteView(BaseAdminDeleteView):
    model = Property
    template_name = "admin/pages/property/index.html"
    success_url = "/admin/properties/"


class PropertyListingView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/listing.html"


class PropertyDetailView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/property_detail.html"


class PropertyView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/form-wizzard/property.html"
