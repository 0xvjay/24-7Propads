from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("title", "body", "score")


class AdminReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("status",)
