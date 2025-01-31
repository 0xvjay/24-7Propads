from django.contrib import admin
from django.utils.html import format_html

from .forms import AdminPropertyForm
from .models import (
    AgricultureLand,
    Flat,
    House,
    Office,
    Plot,
    Property,
    PropertyAttributes,
    PropertyImage,
    PropertyType,
    Villa,
)


@admin.register(PropertyAttributes)
class PropertyAttributesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    search_fields = ("name",)


class AgricultureLandInline(admin.StackedInline):
    model = AgricultureLand
    extra = 0


class FlatInline(admin.StackedInline):
    model = Flat
    extra = 0


class VillaInline(admin.StackedInline):
    model = Villa
    extra = 0


class HouseInline(admin.StackedInline):
    model = House
    extra = 0


class OfficeInline(admin.StackedInline):
    model = Office
    extra = 0


class PlotInline(admin.StackedInline):
    model = Plot
    extra = 0


class PropertyImageInline(admin.StackedInline):
    model = PropertyImage
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = AdminPropertyForm
    list_display = (
        "id",
        "show_image",
        "name",
        "post_type",
        "type",
        "is_active",
        "is_verified",
        "is_featured",
        "is_popular",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    inlines = [
        PropertyImageInline,
        AgricultureLandInline,
        FlatInline,
        VillaInline,
        HouseInline,
        OfficeInline,
        PlotInline,
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def show_image(self, obj):
        property_image = obj.images.first()
        if property_image:
            return format_html(
                '<img src="{}" width=100 />'.format(property_image.image.url)
            )

    show_image.short_description = "Profile"
