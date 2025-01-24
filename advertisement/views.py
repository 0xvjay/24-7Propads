from core.views import (
    BaseAdminCreateView,
    BaseAdminDeleteView,
    BaseAdminListView,
    BaseAdminUpdateView,
)

from .forms import AdvertisementForm
from .models import Advertisement


class AdvertisementCreateView(BaseAdminCreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "admin/pages/advertisement/create.html"
    success_url = "/admin/advertisements/"


class AdvertisementListView(BaseAdminListView):
    model = Advertisement
    template_name = "admin/pages/advertisement/index.html"


class AdvertisementUpdateView(BaseAdminUpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "admin/pages/advertisement/edit.html"
    success_url = "/admin/advertisements/"


class AdvertisementDeleteView(BaseAdminDeleteView):
    model = Advertisement
    template_name = "admin/pages/advertisement/index.html"
    success_url = "/admin/advertisements/"
