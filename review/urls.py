from django.urls import path

from .views import ReviewCreateView, ReviewDeleteView

app_name = "review"
urlpatterns = [
    path(
        r"reviews/<int:property_pk>/add/", ReviewCreateView.as_view(), name="add_review"
    ),
    path(r"reviews/delete/<int:pk>/", ReviewDeleteView.as_view(), name="delete_review"),
]
