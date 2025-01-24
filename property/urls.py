from django.urls import path

from .views import (
    PropertyCreateView,
    PropertyDeleteView,
    PropertyListView,
    PropertyUpdateView,
    TypeCreateView,
    TypeDeleteView,
    TypeListView,
    TypeUpdateView,
    show_agriculture_form,
    show_flat_form,
    show_house_form,
    show_office_form,
    show_plot_form,
    show_villa_form,
    PropertyListingView,
    PropertyView,
    PropertyDetailView,
)

app_name = "property"
urlpatterns = [
    # types
    path(r"admin/types/", TypeListView.as_view(), name="types"),
    path(r"admin/types/add", TypeCreateView.as_view(), name="add_type"),
    path(r"admin/types/edit/<int:pk>/", TypeUpdateView.as_view(), name="edit_type"),
    path(r"admin/types/delete/<int:pk>/", TypeDeleteView.as_view(), name="delete_type"),
    # properties
    path(r"admin/properties/", PropertyListView.as_view(), name="properties"),
    path(
        r"admin/properties/add",
        PropertyCreateView.as_view(
            condition_dict={
                "1": show_agriculture_form,
                "2": show_villa_form,
                "3": show_house_form,
                "4": show_flat_form,
                "5": show_office_form,
                "6": show_plot_form,
            }
        ),
        name="add_property",
    ),
    path(
        r"admin/properties/edit/<int:pk>/",
        PropertyUpdateView.as_view(
            condition_dict={
                "1": show_agriculture_form,
                "2": show_villa_form,
                "3": show_house_form,
                "4": show_flat_form,
                "5": show_office_form,
                "6": show_plot_form,
            }
        ),
        name="edit_property",
    ),
    path(
        r"admin/properties/delete/<int:pk>/",
        PropertyDeleteView.as_view(),
        name="delete_property",
    ),
    path(r"properties/", PropertyListingView.as_view(), name="property_list"),
    path(r"properties/<int:pk>/", PropertyDetailView.as_view(), name="property"),
    path(r"properties/add", PropertyView.as_view(), name="add_customer_property"),
]
