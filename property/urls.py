from django.urls import path

from .views import (
    CustomerPropertyCreateView,
    LikeView,
    PropertyCreateView,
    PropertyDeleteView,
    PropertyDetailView,
    PropertyListingView,
    PropertyListView,
    PropertyUpdateView,
    TypeCreateView,
    TypeDeleteView,
    TypeListView,
    TypeUpdateView,
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
    path(r"admin/properties/add", PropertyCreateView.as_view(), name="add_property"),
    path(
        r"admin/properties/edit/<int:pk>/",
        PropertyUpdateView.as_view(),
        name="edit_property",
    ),
    path(
        r"admin/properties/delete/<int:pk>/",
        PropertyDeleteView.as_view(),
        name="delete_property",
    ),
    path(r"properties/", PropertyListingView.as_view(), name="property_list"),
    path(r"properties/<int:pk>/", PropertyDetailView.as_view(), name="property"),
    path(
        r"properties/add",
        CustomerPropertyCreateView.as_view(),
        name="add_customer_property",
    ),
    path(r"properties/<int:pk>/like", LikeView.as_view(), name="add_like"),
]
