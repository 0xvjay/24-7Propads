from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import DefaultStorage
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, DecimalField, Q, Value
from django.db.models.functions import Coalesce
from django.db.models.functions import Lower as LowerCase
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView
from formtools.wizard.views import SessionWizardView

from analytic.views import PropertyRecommender, UserActivity
from core.views import (
    AdminLoginRequired,
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
from .models import Property, PropertyAttributes, PropertyImage, PropertyType


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
    cleaned_data = wizard.get_cleaned_data_for_step("0")
    user_choice = wizard.request.session.get("user_choice")
    type_data = (
        cleaned_data.get("type")
        if cleaned_data
        else PropertyType.objects.get(id=user_choice)
        if user_choice
        else None
    )
    return type_data and type_data.name == "Agriculture Land"


def show_villa_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0")
    user_choice = wizard.request.session.get("user_choice")
    type_data = (
        cleaned_data.get("type")
        if cleaned_data
        else PropertyType.objects.get(id=user_choice)
        if user_choice
        else None
    )
    return type_data and type_data.name == "Villa/Independent House"


def show_house_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0")
    user_choice = wizard.request.session.get("user_choice")
    type_data = (
        cleaned_data.get("type")
        if cleaned_data
        else PropertyType.objects.get(id=user_choice)
        if user_choice
        else None
    )
    return type_data and type_data.name == "House"


def show_flat_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0")
    user_choice = wizard.request.session.get("user_choice")
    type_data = (
        cleaned_data.get("type")
        if cleaned_data
        else PropertyType.objects.get(id=user_choice)
        if user_choice
        else None
    )
    return type_data and type_data.name == "Flat/Apartment"


def show_office_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0")
    user_choice = wizard.request.session.get("user_choice")
    type_data = (
        cleaned_data.get("type")
        if cleaned_data
        else PropertyType.objects.get(id=user_choice)
        if user_choice
        else None
    )
    return type_data and type_data.name == "Office/Commercial Space"


def show_plot_form(wizard: SessionWizardView):
    cleaned_data = wizard.get_cleaned_data_for_step("0")
    user_choice = wizard.request.session.get("user_choice")
    type_data = (
        cleaned_data.get("type")
        if cleaned_data
        else PropertyType.objects.get(id=user_choice)
        if user_choice
        else None
    )
    return type_data and type_data.name == "Open Plot"


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


class BasePropertyCreateUpdateView(AdminLoginRequired, SessionWizardView):
    file_storage = DefaultStorage()
    form_list = FORMS
    condition_dict = CONDITION_DICT
    success_url = "/admin/properties/"
    templates = None
    storage_name = "property.utils.CustomSessionStorage"

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        return redirect(self.success_url)

    def process_step(self, form):
        if self.steps.current == "0":
            self.request.session["user_choice"] = form.data.get("0-type")

        return super().process_step(form)

    def get(self, request, *args, **kwargs):
        self.storage.current_step = self.steps.first
        return self.render(self.get_form())


class PropertyCreateView(BasePropertyCreateUpdateView):
    templates = {
        "0": "admin/pages/property/create/property.html",
        "1": "admin/pages/property/create/agriculture.html",
        "2": "admin/pages/property/create/villa.html",
        "3": "admin/pages/property/create/house.html",
        "4": "admin/pages/property/create/flat.html",
        "5": "admin/pages/property/create/office.html",
        "6": "admin/pages/property/create/plot.html",
    }

    def done(self, form_list, **kwargs):
        property_form = form_list[0]
        other_form = form_list[1]

        with transaction.atomic():
            property_form.instance.user = self.request.user
            property = property_form.save()

            for image in property_form.cleaned_data.get("images"):
                PropertyImage.objects.create(image=image, property=property)

            other_form.instance.property = property
            other_form.save()

        return super().done(form_list)


class PropertyUpdateView(BasePropertyCreateUpdateView):
    templates = {
        "0": "admin/pages/property/edit/property.html",
        "1": "admin/pages/property/edit/agriculture.html",
        "2": "admin/pages/property/edit/villa.html",
        "3": "admin/pages/property/edit/house.html",
        "4": "admin/pages/property/edit/flat.html",
        "5": "admin/pages/property/edit/office.html",
        "6": "admin/pages/property/edit/plot.html",
    }

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        property_instance = Property.objects.get(id=id)
        self.instance_dict = {
            "0": property_instance,
            "1": property_instance.agriculture_details
            if hasattr(property_instance, "agriculture_details")
            else None,
            "2": property_instance.villa_details
            if hasattr(property_instance, "villa_details")
            else None,
            "3": property_instance.house_details
            if hasattr(property_instance, "house_details")
            else None,
            "4": property_instance.flat_details
            if hasattr(property_instance, "flat_details")
            else None,
            "5": property_instance.office_details
            if hasattr(property_instance, "office_details")
            else None,
            "6": property_instance.plot_details
            if hasattr(property_instance, "plot_details")
            else None,
        }
        return super(PropertyUpdateView, self).dispatch(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        property_form = form_list[0]
        other_form = form_list[1]

        with transaction.atomic():
            if hasattr(self.instance_dict["0"], "agriculture_details"):
                self.instance_dict["0"].agriculture_details.delete()
            elif hasattr(self.instance_dict["0"], "villa_details"):
                self.instance_dict["0"].villa_details.delete()
            elif hasattr(self.instance_dict["0"], "house_details"):
                self.instance_dict["0"].house_details.delete()
            elif hasattr(self.instance_dict["0"], "flat_details"):
                self.instance_dict["0"].flat_details.delete()
            elif hasattr(self.instance_dict["0"], "office_details"):
                self.instance_dict["0"].office_details.delete()
            elif hasattr(self.instance_dict["0"], "plot_details"):
                self.instance_dict["0"].plot_details.delete()

            property_form.instance.user = self.request.user
            property = property_form.save()

            try:
                property.images.all().delete()
            except Exception:
                pass

            for image in property_form.cleaned_data.get("images"):
                PropertyImage.objects.create(image=image, property=property)

            other_form.instance.property = property
            other_form.save()

        return super().done(form_list)


class PropertyDeleteView(BaseAdminDeleteView):
    model = Property
    template_name = "admin/pages/property/index.html"
    success_url = "/admin/properties/"


class PropertyListingView(LoginRequiredMixin, ListView):
    model = Property
    paginate_by = 10
    template_name = "customer/pages/listing.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        location_query = self.request.GET.get("location")
        if location_query:
            queryset = queryset.filter(
                Q(city__icontains=location_query)
                | Q(address__icontains=location_query)
                | Q(state__icontains=location_query)
                | Q(postal_code__icontains=location_query)
                | Q(lat__icontains=location_query)
                | Q(long__icontains=location_query)
            )

        type_query = self.request.GET.get("type")
        if type_query:
            queryset = queryset.filter(Q(type__name__icontains=type_query))

        post_type_query = self.request.GET.get("post_type")
        if post_type_query:
            queryset = queryset.filter(Q(post_type__icontains=post_type_query))

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price and max_price:
            queryset = queryset.annotate(
                price_to_filter=Coalesce(
                    "agriculture_details__price",
                    Coalesce(
                        "flat_details__price",
                        "villa_details__price",
                        "house_details__price",
                        "office_details__price",
                        "plot_details__price",
                        output_field=DecimalField(),
                    ),
                )
            ).filter(price_to_filter__range=(min_price, max_price))
        if min_price and not max_price:
            queryset = queryset.annotate(
                price_to_filter=Coalesce(
                    "agriculture_details__price",
                    Coalesce(
                        "flat_details__price",
                        "villa_details__price",
                        "house_details__price",
                        "office_details__price",
                        "plot_details__price",
                        output_field=DecimalField(),
                    ),
                )
            ).filter(price_to_filter__gte=min_price)
        if max_price and not min_price:
            queryset = queryset.annotate(
                price_to_filter=Coalesce(
                    "agriculture_details__price",
                    Coalesce(
                        "flat_details__price",
                        "villa_details__price",
                        "house_details__price",
                        "office_details__price",
                        "plot_details__price",
                        output_field=DecimalField(),
                    ),
                )
            ).filter(price_to_filter__lte=max_price)

        # min_area = self.request.GET.get("min_area")
        # max_area = self.request.GET.get("max_area")
        # if min_area and max_area:
        #     queryset = queryset.annotate(
        #         area_to_filter=Coalesce(
        #             "agriculture_details__area",
        #             Coalesce(
        #                 "flat_details__area",
        #                 "villa_details__area",
        #                 "house_details__area",
        #                 "office_details__area",
        #                 "plot_details__area",
        #                 output_field=CharField(),
        #             ),
        #         )
        #     ).filter(area_to_filter__range=(min_area, max_area))
        # if min_area and not max_area:
        #     queryset = queryset.annotate(
        #         area_to_filter=Coalesce(
        #             "agriculture_details__area",
        #             Coalesce(
        #                 "flat_details__area",
        #                 "villa_details__area",
        #                 "house_details__area",
        #                 "office_details__area",
        #                 "plot_details__area",
        #                 output_field=CharField(),
        #             ),
        #         )
        #     ).filter(area_to_filter__gte=min_area)
        # if max_area and not min_area:
        #     queryset = queryset.annotate(
        #         area_to_filter=Coalesce(
        #             "agriculture_details__area",
        #             Coalesce(
        #                 "flat_details__area",
        #                 "villa_details__area",
        #                 "house_details__area",
        #                 "office_details__area",
        #                 "plot_details__area",
        #                 output_field=CharField(),
        #             ),
        #         )
        #     ).filter(area_to_filter__lte=max_area)

        sort_by = self.request.GET.get("sort")
        if sort_by == "price":
            queryset = queryset.annotate(
                price_to_sort=Coalesce(
                    "agriculture_details__price",
                    Coalesce(
                        "flat_details__price",
                        "villa_details__price",
                        "house_details__price",
                        "office_details__price",
                        "plot_details__price",
                        output_field=DecimalField(),
                    ),
                )
            ).order_by("price_to_sort")
        elif sort_by == "-price":
            queryset = queryset.annotate(
                price_to_sort=Coalesce(
                    "agriculture_details__price",
                    Coalesce(
                        "flat_details__price",
                        "villa_details__price",
                        "house_details__price",
                        "office_details__price",
                        "plot_details__price",
                        output_field=DecimalField(),
                    ),
                )
            ).order_by("-price_to_sort")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_properties"] = Property.objects.all()[:5]

        cities = ["hyderabad", "vijaywada", "bangalore", "chennai"]

        context.update({f"{city.lower()}_count": 0 for city in cities})
        for city, count in (
            Property.objects.annotate(lower_city=LowerCase("city"))
            .filter(lower_city__in=cities)
            .values("city")
            .annotate(count=Coalesce(Count("id"), Value(0)))
            .values_list("city", "count")
        ):
            context[f"{city.lower()}_count"] = count

        recommender = PropertyRecommender(self.request.user)
        context["recommended_properties"] = recommender.get_recommendations(top_n=5)
        return context


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = "customer/pages/property_detail.html"

    def get(self, request, *args, **kwargs):
        user_activity = UserActivity(request.user)
        property = self.get_object()
        user_activity.record_property_view(property)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.get_object().reviews.all(), 5)
        page_number = self.request.GET.get("page")
        context["reviews"] = paginator.get_page(page_number)

        recommender = PropertyRecommender(self.request.user)
        context["recommended_properties"] = recommender.get_recommendations(top_n=5)
        return context


class CustomerPropertyCreateView(LoginRequiredMixin, SessionWizardView):
    file_storage = DefaultStorage()
    form_list = FORMS
    condition_dict = CONDITION_DICT
    storage_name = "property.utils.CustomSessionStorage"
    templates = {
        "0": "customer/pages/form-wizzard/property.html",
        "1": "customer/pages/form-wizzard/agriculture.html",
        "2": "customer/pages/form-wizzard/villa.html",
        "3": "customer/pages/form-wizzard/house.html",
        "4": "customer/pages/form-wizzard/flat.html",
        "5": "customer/pages/form-wizzard/office.html",
        "6": "customer/pages/form-wizzard/plot.html",
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        property_form = form_list[0]
        other_form = form_list[1]

        with transaction.atomic():
            property_form.instance.user = self.request.user
            property = property_form.save()

            for image in property_form.cleaned_data.get("images"):
                PropertyImage.objects.create(image=image, property=property)

            other_form.instance.property = property
            other_form.save()

        return redirect(f"/properties/{property.id}")

    def process_step(self, form):
        if self.steps.current == "0":
            self.request.session["user_choice"] = form.data.get("0-type")
        return super().process_step(form)

    def get(self, request, *args, **kwargs):
        self.storage.current_step = self.steps.first
        return self.render(self.get_form())


class LikeView(LoginRequiredMixin, TemplateView):
    template_name = "customer/pages/listing.html"
    success_url = "/properties/"

    def get(self, request, *args, **kwargs):
        property_pk = kwargs.pop("pk")
        if not property_pk:
            messages.error(request, "Bad Request")
            return redirect(self.success_url)

        property = Property.objects.filter(id=property_pk).first()
        if not property:
            messages.error(request, "Bad Request")
            return redirect(self.success_url)

        user_activity = UserActivity(request.user)
        user_activity.like_property(property)

        return redirect(self.success_url)
