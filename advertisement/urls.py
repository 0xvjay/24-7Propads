from django.urls import path

from .views import (
    AdvertisementCreateView,
    AdvertisementDeleteView,
    AdvertisementListView,
    AdvertisementUpdateView,
)

app_name = "advertisement"

urlpatterns = [
    path(
        r"admin/advertisements/", AdvertisementListView.as_view(), name="advertisements"
    ),
    path(
        r"admin/advertisements/add",
        AdvertisementCreateView.as_view(),
        name="add_advertisement",
    ),
    path(
        r"admin/advertisements/edit/<int:pk>/",
        AdvertisementUpdateView.as_view(),
        name="edit_advertisement",
    ),
    path(
        r"admin/advertisements/delete/<int:pk>/",
        AdvertisementDeleteView.as_view(),
        name="delete_advertisement",
    ),
]
