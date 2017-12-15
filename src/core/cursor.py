"""
Copied from https://gist.github.com/mjtamlyn/e8e03d78764552289ea4e2155c554deb
"""

import functools

from django.db.models import Prefetch, QuerySet

import attr
import graphene
from graphene.utils.str_converters import to_snake_case
from graphene_django.filter import DjangoFilterConnectionField
from cursor_pagination import CursorPaginator
from graphql_relay import connection_from_list

from .optimization import get_fields, get_node_type


@attr.s
class PageQuery(object):
    before = attr.ib()
    after = attr.ib()
    first = attr.ib()
    last = attr.ib()


def connection_from_cursor_paginated(queryset, connection_type, edge_type, pageinfo_type, page_query=None):
    """Create a Connection object from a queryset, using CursorPaginator"""
    paginator = CursorPaginator(queryset, queryset.query.order_by)
    if page_query is None:
        page_query = PageQuery()
    page = paginator.page(
        **attr.asdict(page_query)
    )

    edges = []
    for item in list(page):
        edge = edge_type(node=item, cursor=paginator.cursor(item))
        edges.append(edge)

    if page:
        page_info = pageinfo_type(
            start_cursor=paginator.cursor(edges[0].node),
            end_cursor=paginator.cursor(edges[-1].node),
            has_previous_page=page.has_previous,
            has_next_page=page.has_next,
        )
    else:
        page_info = pageinfo_type(
            start_cursor=None,
            end_cursor=None,
            has_previous_page=False,
            has_next_page=False,
        )

    return connection_type(
        edges=edges,
        page_info=page_info,
    )


def apply_optimizers(queryset, node_type, subfields, info, post_processors):
    """Apply optimisations the a given queryset.

    This function calls itself recursively to follow the GraphQL tree down,
    looking at node_type to find functions it can call to improve the queryset
    before execution.
    """
    # Firstly, look for any `dependant_fields_FOO` functions
    # These functions allow additional fields to be optimised for if FOO
    # exists.
    for field_name, details in subfields.items():
        field_name = to_snake_case(field_name)
        dependant_fields_getter = getattr(
            node_type, 'dependant_fields_%s' % field_name, None)
        if dependant_fields_getter is not None:
            dependant_fields = dependant_fields_getter()
            for dependant_field, dependant_subfields in dependant_fields.items():
                if dependant_field not in subfields:
                    subfields[dependant_field] = {'fields': {}}
                for subfield in dependant_subfields:
                    if subfield not in subfields[dependant_field]['fields']:
                        subfields[dependant_field]['fields'][subfield] = {}

    # The meat of the problem - apply optimizers
    for field_name, details in subfields.items():
        field_name = to_snake_case(field_name)
        # If the field has subfields, and is a node, then recurse and apply as a prefetch_related
        if details.get('fields'):
            related_node_type = get_node_type(
                node_type._meta.fields[field_name])
            if related_node_type:
                model = related_node_type._meta.model
                related_queryset = apply_optimizers(model.objects.all(
                ), related_node_type, details['fields'], info, post_processors)
                # The node can also have a custom `prefetch_FOO` function to customise the way a prefetch_related is applied
                prefetcher = getattr(
                    node_type, 'prefetch_%s' % field_name, None)
                if prefetcher is not None:
                    queryset = prefetcher(queryset, related_queryset)
                elif isinstance(queryset, QuerySet):
                    print('Automatic prefetch of {}'.format(field_name))
                    queryset = queryset.prefetch_related(
                        Prefetch(field_name, queryset=related_queryset))

        # Now look for any field-specific optimizers, and apply them.
        # These are called `optimize_FOO`, and take the queryset, info,
        # subfields if they are present, and any arguments
        optimizer = getattr(node_type, 'optimize_%s' % field_name, None)
        if optimizer is not None:
            kwargs = {'queryset': queryset, 'info': info}
            if 'fields' in details:
                kwargs['subfields'] = details['fields']
            if 'arguments' in details:
                kwargs.update(details['arguments'])
            print('optimize_{} called'.format(field_name))
            queryset = optimizer(**kwargs)

        # Now look for any subfield-specific optimizers, and apply them
        # These are called `optimize_FOO__BAR`, and take the queryset, info,
        # subfields if they are present, and any arguments
        for subfield_name in details.get('fields', []):
            optimizer = getattr(node_type, 'optimize_%s__%s' %
                                (field_name, subfield_name), None)
            if optimizer is not None:
                kwargs = {'queryset': queryset, 'info': info}
                if details.get('arguments'):
                    kwargs.update(details['arguments'])
                queryset = optimizer(**kwargs)

        # Finally, look for any `post_process_FOO` functions and collect them
        post_processor = getattr(
            node_type, 'post_process_%s' % field_name, None)
        if post_processor:
            post_processors.append(post_processor)
    return queryset


def node_fields_are_queried(fields, key):
    """Utility function to check if any subfields are needed."""
    node_fields = fields[key].get('fields', {}).get('edges', {}).get(
        'fields', {}).get('node', {}).get('fields', {})
    if node_fields:
        return True
    return False


def optimize_qs(connection_type, queryset, info=None, fields=None, post_processors=None):
    """Apply optimisations to the queryset based on the fields queried."""
    if fields is None:
        fields = get_fields(info.field_asts, info)
    key = next(iter(fields))
    if not node_fields_are_queried(fields, key):
        return queryset
    if post_processors is None:
        post_processors = []
    subfields = fields[key]['fields']['edges']['fields']['node']['fields']
    node_type = connection_type._meta.node
    queryset = apply_optimizers(
        queryset, node_type, subfields, info, post_processors)
    return queryset, post_processors


def apply_ordering(queryset, **kwargs):
    """ Apply ordering to the queryset. 

        The 'orderBy' kwarg is used - if defined;
        otherwise the model's 'ordering' meta field is used - if defined;
        otherwise we default to ordering by descending id
    """
    if 'orderBy' in kwargs:
        order_by_field = kwargs.get('orderBy')
        # CursorPaginator requires all order_by fields to be in the same direction and the
        # data must be ordered by fields which are unique across all records.
        id_order = '-id' if order_by_field.startswith('-') else 'id'
        return queryset.order_by(order_by_field, id_order)
    elif queryset.model._meta.ordering:
        id_order = '-id' if queryset.model._meta.ordering[0].startswith(
            '-') else 'id'
        return queryset.order_by(*queryset.model._meta.ordering, id_order)
    else:
        return queryset.order_by('-id')


class CursorPaginatedConnectionField(DjangoFilterConnectionField):
    def __init__(self, *args, **kwargs):
        kwargs['resolver'] = self.cursor_resolver
        kwargs.setdefault('before', graphene.String())
        kwargs.setdefault('after', graphene.String())
        kwargs.setdefault('first', graphene.Int())
        kwargs.setdefault('last', graphene.Int())
        kwargs.setdefault('orderBy', graphene.String())
        super().__init__(*args, **kwargs)

    def cursor_resolver(self, instance, info, parent_resolver=None, before=None, after=None, first=None, last=None, **kwargs):
        if parent_resolver:
            qs = parent_resolver(instance, info, **kwargs)
            qs = apply_ordering(qs, **kwargs)
        else:
            qs = instance.items
        if isinstance(qs, self.type):
            return qs
        page_query = PageQuery(
            before=before, after=after, first=first, last=last)
        queryset, post_processors = optimize_qs(self.type, qs, info)

        # Filtering - copied from DjangoFilterConnectionField.connection_resolver
        filter_kwargs = {k: v for k,
                         v in kwargs.items() if k in self.filtering_args}
        queryset = self.filterset_class(
            data=filter_kwargs,
            queryset=queryset,
        ).qs
        # End of filtering

        if isinstance(qs, list):
            connection = connection_from_list(
                queryset,
                connection_type=self.type,
                edge_type=self.type.Edge,
                pageinfo_type=graphene.relay.PageInfo,
                args=attr.asdict(page_query),
            )
        else:
            connection = connection_from_cursor_paginated(
                queryset,
                connection_type=self.type,
                edge_type=self.type.Edge,
                pageinfo_type=graphene.relay.PageInfo,
                page_query=page_query,
            )
        # Post processors currently only work when the processor model is the
        # topmost model, behaviour below that is undefined and may break
        for processor in post_processors:
            processor([edge.node for edge in connection.edges], info)
        return connection

    def get_resolver(self, parent_resolver):
        return functools.partial(self.cursor_resolver, parent_resolver=parent_resolver)
