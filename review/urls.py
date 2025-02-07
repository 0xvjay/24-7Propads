from django.urls import path

from .views import ReviewCreateView, ReviewDeleteView, ReviewListView, ReviewEditView

app_name = "review"
urlpatterns = [
    path(
        r"reviews/<int:property_pk>/add/", ReviewCreateView.as_view(), name="add_review"
    ),
    path(r"reviews/delete/<int:pk>/", ReviewDeleteView.as_view(), name="delete_review"),
    path(
        r"reviews/<int:property_pk>/", ReviewListView.as_view(), name="property_reviews"
    ),
    path(
        r"reviews/<int:property_pk>/edit/<int:pk>/",
        ReviewEditView.as_view(),
        name="edit_review",
    ),
]
