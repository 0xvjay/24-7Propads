from django.db import models

from accounts.models import User


class TransactionType(models.TextChoices):
    NEW_PROPERTY = "New Property"
    RESALE_PROPERTY = "Resale Property"


class PossessionType(models.TextChoices):
    READY_TO_MOVE = "Ready To Move"
    UNDER_CONSTRUCTION = "Under Contruction"


class FurnishingType(models.TextChoices):
    FURNISHED = "Furnished"
    SEMI_FURNISHED = "Semi-Furnished"
    UNFURNISHED = "Unfurnished"


class PropertyAttributes(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Property Attributes"


class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    attributes = models.ManyToManyField(
        PropertyAttributes, related_name="attributes", blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Property Types"


class Property(models.Model):
    class PostType(models.TextChoices):
        SALE = "Sale"
        LEASE = "Lease"
        RENT = "Rent"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    name = models.CharField(max_length=255)
    post_type = models.CharField(choices=PostType.choices, max_length=20)
    type = models.ForeignKey(
        PropertyType, related_name="properties", on_delete=models.SET_NULL, null=True
    )
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=30)
    image = models.ImageField(upload_to="properties/")

    # address
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=6)

    # SEO
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    is_rera_agent = models.BooleanField()
    rera_number = models.CharField(max_length=255, null=True, blank=True)

    #
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def details(self):
        if hasattr(self, "agriculture_details"):
            return self.agriculture_details
        elif hasattr(self, "flat_details"):
            return self.flat_details
        elif hasattr(self, "villa_details"):
            return self.villa_details
        elif hasattr(self, "plot_details"):
            return self.plot_details
        elif hasattr(self, "office_details"):
            return self.office_details
        elif hasattr(self, "house_details"):
            return self.house_details
        else:
            None

    def __str__(self):
        return f"{self.name} ({self.post_type} - {self.type})"

    class Meta:
        verbose_name_plural = "Properties"


class BaseProperty(models.Model):
    class FacingType(models.TextChoices):
        EAST = "East"
        WEST = "West"
        NORTH = "North"
        SOUTH = "South"

    class CommissionType(models.TextChoices):
        POINT_FIVE_PERCENT = ".5% of Sale Amount"
        ONE_PERCENT = "1.0% of Sale Amount"
        ONE_HALF_PERCENT = "1.5% of Sale Amount"
        TWO_PERCENT = "2.0% of Sale Amount"
        CONTACT_ME = "Contact Me For Details"
        NOT_APPLICABLE = "Not Applicable"

    facing = models.CharField(choices=FacingType.choices, max_length=20)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.CharField(choices=CommissionType.choices, max_length=200)

    class Meta:
        abstract = True


class Flat(BaseProperty):
    class ApartmentType(models.TextChoices):
        STANDALONE_APARTMENT = "Standalone Apartment"
        GATED_COMMUNITY = "Gated Community"

    class ModelType(models.TextChoices):
        SIMPLEX_FLAT = "Simplex Flat"
        DUPLEX_FLAT = "Duplex Flat"
        TRIPLEX_FLAT = "Triplex Flat"

    property = models.OneToOneField(
        Property, related_name="flat_details", on_delete=models.CASCADE
    )
    apartment = models.CharField(choices=ApartmentType.choices, max_length=100)
    model = models.CharField(choices=ModelType.choices, max_length=50)
    transaction = models.CharField(choices=TransactionType.choices, max_length=100)
    possession = models.CharField(choices=PossessionType.choices, max_length=100)
    available_from = models.DateField()
    age = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=255)
    undivided_share = models.CharField(max_length=255)
    furnish = models.CharField(choices=FurnishingType.choices, max_length=50)
    bathrooms = models.PositiveSmallIntegerField()
    balconies = models.PositiveSmallIntegerField()
    total_floors = models.PositiveSmallIntegerField()
    floor_no = models.PositiveSmallIntegerField()
    car_parking = models.PositiveSmallIntegerField()
    maintenance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.property.name} - Flat"


class Villa(BaseProperty):
    class ModelType(models.TextChoices):
        SIMPLEX_FLAT = "Simplex Flat"
        DUPLEX_FLAT = "Duplex Flat"
        TRIPLEX_FLAT = "Triplex Flat"

    property = models.OneToOneField(
        Property, related_name="villa_details", on_delete=models.CASCADE
    )
    model = models.CharField(choices=ModelType.choices, max_length=50)
    transaction = models.CharField(choices=TransactionType.choices, max_length=100)
    possession = models.CharField(choices=PossessionType.choices, max_length=100)
    available_from = models.DateField()
    age = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=255)
    plot_area = models.CharField(max_length=255)
    approach_road = models.CharField(max_length=255)
    furnish = models.CharField(choices=FurnishingType.choices, max_length=50)
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    balconies = models.PositiveSmallIntegerField()
    car_parking = models.PositiveSmallIntegerField()
    maintenance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.property.name} - Villa"


class Plot(BaseProperty):
    class Type(models.TextChoices):
        RESIDENTIAL_PLOT_IN_COLONY = "Residential Plot In Colony/Society"
        RESIDENTIAL_PLOT_IN_GATED_COMMUNITY = "Residential Plot In Gated Community"
        FARM_LAND_PLOT = "Farm Land Plot"
        COMMERCIAL_PLOT_IN_COLONY = "Commercial Plot In Colony/Society"
        COMMERCIAL_PLOT_IN_GATED_COMMUNITY = "Commercial Plot In Gated Community"

    property = models.OneToOneField(
        Property, related_name="plot_details", on_delete=models.CASCADE
    )
    type = models.CharField(choices=Type.choices, max_length=100)
    authority = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    length = models.CharField(max_length=255)
    breadth = models.CharField(max_length=255)
    approach_road = models.CharField(max_length=255)
    maintenance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.property.name} - Plot"


class Office(BaseProperty):
    class Type(models.TextChoices):
        RETAIL_SHOP = "Retail Shop"
        OFFICE_SPACE = "Office Space"
        PLUG_AND_PLAY_OFFICE_SPACE = "Plug and Play Office Space"

    property = models.OneToOneField(
        Property, related_name="office_details", on_delete=models.CASCADE
    )
    type = models.CharField(choices=Type.choices, max_length=100)
    transaction = models.CharField(choices=TransactionType.choices, max_length=100)
    possession = models.CharField(choices=PossessionType.choices, max_length=100)
    available_from = models.DateField()
    age = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=255)
    plot_area = models.CharField(max_length=255)
    undivided_share = models.CharField(max_length=255)
    furnish = models.CharField(choices=FurnishingType.choices, max_length=50)
    seating_capacity = models.PositiveSmallIntegerField()
    total_floors = models.PositiveSmallIntegerField()
    floor_no = models.PositiveSmallIntegerField()
    car_parking = models.PositiveSmallIntegerField()
    maintenance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.property.name} - Office"


class House(BaseProperty):
    class ModelType(models.TextChoices):
        GROUND_FLOOR = "Ground Floor"
        GROUND_PLUS_ONE_FLOORS = "Ground + 1 Floors"
        GROUND_PLUS_TWO_FLOORS = "Ground + 2 Floors"
        GROUND_PLUS_THREE_FLOORS = "Ground + 3 Floors"
        GROUND_PLUS_FOUR_FLOORS = "Ground + 4 Floors"
        GROUND_PLUS_FIVE_FLOORS = "Ground + 5 Floors"
        GROUND_PLUS_SIX_FLOORS = "Ground + 6 Floors"
        GROUND_PLUS_SIX_PLUS_FLOORS = "Ground + 6 Floors +"

    property = models.OneToOneField(
        Property, related_name="house_details", on_delete=models.CASCADE
    )
    model = models.CharField(choices=ModelType.choices, max_length=100)
    transaction = models.CharField(choices=TransactionType.choices, max_length=100)
    possession = models.CharField(choices=PossessionType.choices, max_length=100)
    available_from = models.DateField()
    age = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=255)
    plot_area = models.CharField(max_length=255)
    approach_road = models.CharField(max_length=255)
    furnish = models.CharField(choices=FurnishingType.choices, max_length=50)
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    balconies = models.PositiveSmallIntegerField()
    car_parking = models.PositiveSmallIntegerField()
    maintenance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.property.name} - House"


class AgricultureLand(BaseProperty):
    property = models.OneToOneField(
        Property, related_name="agriculture_details", on_delete=models.CASCADE
    )
    acres = models.CharField(max_length=255)
    approach_road = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.property.name} - Agriculture"
