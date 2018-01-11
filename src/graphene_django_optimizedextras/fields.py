"""
Field definitions for graphene_django_optimizedextras
"""
from functools import partial
from graphene.utils.str_converters import to_snake_case
from graphene_django.utils import maybe_queryset, is_valid_django_model
from graphene_django_extras.registry import get_global_registry
from graphene_django_extras.utils import get_extra_filters
from graphene_django_extras.base_types import DjangoListObjectBase
from graphene_django_extras.fields import DjangoFilterPaginateListField, DjangoListObjectField
from graphene_django_extras.paginations.utils import _get_count
from .utils import queryset_factory, get_prefetched_attr

registry = get_global_registry()


class OptimizedDjangoFilterPaginateListField(DjangoFilterPaginateListField):
    """ Adds intelligent optimization to the graphene_django_extra's DjangoFilterPaginateListField """

    def get_queryset(self, root, field_name, field_asts, fragments, **kwargs):
        prefetched = get_prefetched_attr(root, to_snake_case(field_name))
        if prefetched:
            print('Using prefetched', field_name)
            return prefetched

        filter_kwargs = {k: v for k,
                         v in kwargs.items() if k in self.filtering_args}
        qs = queryset_factory(self.type.of_type, field_asts,
                              fragments, **kwargs)
        qs = self.filterset_class(data=filter_kwargs, queryset=qs).qs

        return maybe_queryset(qs)

    def list_resolver(self, manager, filterset_class, filtering_args,
                      root, info, **kwargs):

        qs = self.get_queryset(root, info.field_name,
                               info.field_asts, info.fragments, **kwargs)

        # If we've prefetched the queryset, it will be a list object and we don't need to appy the extra filters
        if not isinstance(qs, list) and root and is_valid_django_model(root._meta.model):
            extra_filters = get_extra_filters(root, manager.model)
            qs = qs.filter(**extra_filters)

        if getattr(self, 'pagination', None):
            qs = self.pagination.paginate_queryset(qs, **kwargs)

        return maybe_queryset(qs)


class OptimizedDjangoListObjectField(DjangoListObjectField):

    def __init__(self, *args, **kwargs):
        self.pre_optimize = kwargs.pop('pre_optimize', None)
        self.post_optimize = kwargs.pop('post_optimize', None)
        super(OptimizedDjangoListObjectField, self).__init__(*args, **kwargs)

    def get_queryset(self, root, field_name, field_asts, fragments, **kwargs):
        prefetched = get_prefetched_attr(root, to_snake_case(field_name))
        if prefetched:
            return prefetched

        filter_kwargs = {k: v for k,
                         v in kwargs.items() if k in self.filtering_args}
        qs = queryset_factory(registry.get_type_for_model(self.type._meta.model), field_asts,
                              fragments, **kwargs)
        qs = self.filterset_class(data=filter_kwargs, queryset=qs).qs

        if self.post_optimize:
            qs = self.post_optimize(qs, **kwargs)

        return maybe_queryset(qs)

    def list_resolver(self, manager, filterset_class, filtering_args, root, info, **kwargs):

        qs = self.get_queryset(root, info.field_name,
                               info.field_asts, info.fragments, **kwargs)

        # If we've prefetched the queryset, it will be a list object and we don't need to appy the extra filters
        if not isinstance(qs, list) and root and is_valid_django_model(root._meta.model):
            extra_filters = get_extra_filters(root, manager.model)
            qs = qs.filter(**extra_filters)

        count = _get_count(qs)

        return DjangoListObjectBase(
            count=count,
            results=maybe_queryset(qs),
            results_field_name=self.type._meta.results_field_name
        )
