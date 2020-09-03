"""
Reusable filter classes and utilities
"""

import django_filters
# from django.utils import six
import six

class AndFilter(django_filters.FilterSet):
    """
    A filterset class that combines all filters into a single filter() call
    so that the queryset returns entries that match ALL filters, not just ANY 
    filter.
    """

    @property
    def qs(self):
        """ 
        Returns the queryset with the filters applied.

        Note: This is a direct copy of django_filters.filterset.BaseFilterSet
        with the addition of _next_is_sticky() in front of each filter() call.
        This ensures we end up with a single filter() call on the queryset and 
        query for results that match ALL filters, not ANY filter.

        Ref: https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
        """
        if not hasattr(self, '_qs'):
            if not self.is_bound:
                self._qs = self.queryset.all()
                return self._qs

            if not self.form.is_valid():
                if self.strict == django_filters.constants.STRICTNESS.RAISE_VALIDATION_ERROR:
                    raise django_filters.forms.ValidationError(
                        self.form.errors)
                elif self.strict == django_filters.constants.STRICTNESS.RETURN_NO_RESULTS:
                    self._qs = self.queryset.none()
                    return self._qs
                # else STRICTNESS.IGNORE...  ignoring

            # start with all the results and filter from there
            qs = self.queryset.all()
            for name, filter_ in six.iteritems(self.filters):
                value = self.form.cleaned_data.get(name)

                if value is not None:  # valid & clean data
                    # Add _next_is_sticky() call to keep all filters together
                    qs = filter_.filter(qs._next_is_sticky(), value)

            self._qs = qs

        return self._qs
