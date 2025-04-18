import django_filters

from .models import Event

class EventFilter(django_filters.FilterSet):
    participant = django_filters.BooleanFilter(method='filter_by_participation', label='Filter by participation')

    class Meta:
        model = Event
        fields = ['participant']

    def filter_by_participation(self, queryset, name, value):
        user = self.request.user

        if user.is_authenticated and value is True:
            return queryset.filter(participant=user)
        elif user.is_authenticated and value is False:
            return queryset.exclude(participant=user)

        return queryset
