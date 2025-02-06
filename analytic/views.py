from django.db import transaction
from django.db.models import Q

from accounts.models import User
from property.models import Property

from .models import BrowsingHistory, LikeHistory, SearchHistory


class UserActivity:
    def __init__(self, user: User):
        self.user = user

    @transaction.atomic
    def record_property_view(self, property):
        try:
            BrowsingHistory.objects.get_or_create(user=self.user, property=property)
        except Exception:
            pass

    def record_search(self, **kwargs):
        SearchHistory.objects.get_or_create(user=self.user, **kwargs)

    @transaction.atomic
    def like_property(self, property):
        try:
            like = LikeHistory.objects.get(user=self.user, property=property)
            like.delete()
        except LikeHistory.DoesNotExist:
            LikeHistory.objects.create(user=self.user, property=property)

    def get_recent_browsing(self, limit=10):
        return BrowsingHistory.objects.filter(user=self.user).order_by("-timestamp")[
            :limit
        ]

    def get_recent_search(self, limit=10):
        return SearchHistory.objects.filter(user=self.user).order_by("-timestamp")[
            :limit
        ]


class PropertyRecommender:
    """
    Recommends properties to users based on their activity history.
    """

    def __init__(self, user: User):
        self.user = user

    def get_recommendations(self, top_n=5):
        """
        Fetches and ranks property recommendations for the user.

        Args:
            top_n: The number of recommendations to return.

        Returns:
            A list of recommended Property objects, ranked by relevance.
        """

        recommendations = self._get_browsing_history_recommendations()
        recommendations.update(self._get_liked_history_recommendations())
        recommendations.update(self._get_search_history_recommendations())

        sorted_recommendations = sorted(
            recommendations.items(), key=lambda item: item[1], reverse=True
        )
        return [prop for prop, _ in sorted_recommendations][:top_n]

    def _get_browsing_history_recommendations(self):
        """Recommends properties similar to recently browsed ones."""

        recent_browsing = BrowsingHistory.objects.filter(user=self.user).order_by(
            "-timestamp"
        )[:5]

        recommendations = {}
        for browsing in recent_browsing:
            similar_properties = self._find_similar_properties(browsing.property)
            for prop, score in similar_properties.items():
                recommendations[prop] = recommendations.get(prop, 0) + score
        return recommendations

    def _get_liked_history_recommendations(self):
        """Recommends properties similar to liked ones."""

        liked_properties = LikeHistory.objects.filter(user=self.user).values_list(
            "property", flat=True
        )

        recommendations = {}
        for property_id in liked_properties:
            similar_properties = self._find_similar_properties(
                Property.objects.get(pk=property_id)
            )
            for prop, score in similar_properties.items():
                recommendations[prop] = recommendations.get(prop, 0) + score
        return recommendations

    def _get_search_history_recommendations(self):
        """Recommends properties based on recent search queries."""

        recent_searches = SearchHistory.objects.filter(user=self.user).order_by(
            "-timestamp"
        )[:3]

        recommendations = {}
        for search in recent_searches:
            filters = Q()
            if search.query:
                filters |= Q(name__icontains=search.query) | Q(
                    description__icontains=search.query
                )
            if search.type:
                filters |= Q(type__name__icontains=search.type)
            if search.post_type:
                filters |= Q(post_type__icontains=search.post_type)
            if search.location:
                filters |= (
                    Q(state__icontains=search.location)
                    | Q(city__icontains=search.location)
                    | Q(lat__icontains=search.location)
                    | Q(long__icontains=search.location)
                    | Q(address__icontains=search.location)
                    | Q(postal_code__icontains=search.location)
                )
            if search.price_min:
                filters |= Q(price__gte=search.price_min)
            if search.price_max:
                filters |= Q(price__lte=search.price_max)

            properties = Property.objects.filter(filters)
            for prop in properties:
                recommendations[prop] = recommendations.get(prop, 0) + 1
        return recommendations

    def _find_similar_properties(self, property: Property):
        """Finds properties similar to a given property based on city, state, type, post_type and price."""

        similar_properties = {}
        filters = (
            Q(type__name__icontains=property.type.name)
            | Q(post_type__icontains=property.post_type)
            | Q(city__icontains=property.city)
            | Q(state__icontains=property.state)
            | Q(postal_code__icontains=property.postal_code)
        )
        similar_qs = Property.objects.filter(filters).exclude(pk=property.pk)

        for prop in similar_qs:
            score = 1
            price_diff = abs(property.details.price - prop.details.price)
            score *= 1 / (price_diff + 1)
            similar_properties[prop] = score
        return similar_properties
