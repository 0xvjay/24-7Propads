from django.contrib import messages
from django.shortcuts import redirect

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

    def get(self, request, *args, **kwargs):
        is_allowed, error_message = request.user.can_add_advertisement()

        if not is_allowed:
            messages.error(request, error_message)
            return redirect("/admin/advertisements/")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.object = instance
        return redirect(self.get_success_url())


class AdvertisementListView(BaseAdminListView):
    model = Advertisement
    template_name = "admin/pages/advertisement/index.html"


class AdvertisementUpdateView(BaseAdminUpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "admin/pages/advertisement/edit.html"
    success_url = "/admin/advertisements/"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.object = instance
        return redirect(self.get_success_url())


class AdvertisementDeleteView(BaseAdminDeleteView):
    model = Advertisement
    template_name = "admin/pages/advertisement/index.html"
    success_url = "/admin/advertisements/"
