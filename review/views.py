from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.views import AdminLoginRequired

from .forms import AdminReviewForm, ReviewForm
from .models import Review


class ReviewListView(AdminLoginRequired, ListView):
    model = Review
    template_name = "admin/pages/property/reviews.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(property__pk=self.kwargs.get("property_pk"))
        return qs


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "customer/pages/property_detail.html"
    success_url = "/properties/"

    def post(self, request, *args, **kwargs):
        property_pk = kwargs.pop("property_pk")

        form = self.get_form()

        if not property_pk:
            return self.form_invalid(form)

        if form.is_valid():
            return self.form_valid(form, property_pk)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, property_pk):
        form.instance.property_id = property_pk
        form.instance.user = self.request.user
        self.object = form.save()

        messages.success(self.request, "Review added successfully")

        return redirect(f"{self.success_url}{property_pk}")


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "customer/pages/customer/dashboard.html"


class ReviewEditView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = AdminReviewForm
    template_name = "admin/pages/property/reviews.html"

    def get_success_url(self):
        return f"/reviews/{self.kwargs.get('property_pk')}"
