"""
  Utilities for graphene_django_optimizedextras
"""
from django.db.models import Prefetch
from graphene.utils.str_converters import to_snake_case
from graphene_django_extras import PageGraphqlPagination
from graphene_django_extras.utils import _get_queryset, get_related_fields


def get_paginator():
    """ Convenience factory method for getting a new paginator object """
    return PageGraphqlPagination(page_size_query_param='page_size')


def get_prefetched_attr_name(field_name):
    """ Get the name of the attribute where a prefetched result will be stored """
    return "_prefetched_{}".format(field_name)


def get_prefetched_attr(root, field_name, default=None):
    """ Get the prefetched value corresponding to the given field name (if it exists) """
    return getattr(root, get_prefetched_attr_name(field_name), default)


def get_node_field(root_field, node_name):
    attr_node = getattr(root_field, node_name, None)
    if attr_node:
        return attr_node.type.of_type
    wrapper = root_field._meta.fields[node_name].type().type
    if hasattr(wrapper, '_meta'):
        return wrapper
    return wrapper.of_type


def recursive_optimize(root_field, selection_set, fragments, available_related_fields, select_related, prefetch_related, prefixes=[]):
    has_sub_nodes = False
    for field in selection_set.selections:
        temp = available_related_fields.get(
            field.name.value,
            available_related_fields.get(
                to_snake_case(field.name.value),
                None)
        )
        if temp:
            has_sub_nodes = True
            if temp.many_to_many or temp.one_to_many:
                related_field = getattr(root_field, temp.name)
                kwargs = dict([to_snake_case(i.name.value), i.value.value]
                              for i in field.arguments)
                queryset = related_field.get_queryset(
                    root_field, temp.name, [field], fragments, **kwargs)
                field_prefetch = Prefetch(
                    temp.name, to_attr=get_prefetched_attr_name(temp.name), queryset=queryset)
                prefetch_related.append(field_prefetch)
            else:
                sub_node = get_node_field(root_field, temp.name)
                sub_prefixes = prefixes + [to_snake_case(temp.name)]
                recursive_optimize(
                    sub_node,
                    field.selection_set,
                    fragments,
                    get_related_fields(temp.related_model),
                    select_related,
                    prefetch_related,
                    sub_prefixes
                )
        elif getattr(field, 'selection_set', None):
            recursive_optimize(
                root_field,
                field.selection_set,
                fragments,
                available_related_fields,
                select_related,
                prefetch_related,
                prefixes
            )

    if not has_sub_nodes and prefixes:
        select_related.append("__".join(prefixes))


def queryset_factory(root_field, fields_asts=None, fragments=None, **kwargs):
    manager = root_field._meta.model.objects
    select_related = []
    prefetch_related = []
    available_related_fields = get_related_fields(root_field._meta.model)

    for f in kwargs.keys():
        temp = available_related_fields.get(f.split('_', 1)[0], None)
        if temp:
            if (temp.many_to_many or temp.one_to_many) and \
               temp.name not in prefetch_related:
                prefetch_related.append(temp.name)
            else:
                select_related.append(temp.name)

    if fields_asts:
        recursive_optimize(
            root_field,
            fields_asts[0].selection_set,
            fragments,
            available_related_fields,
            select_related,
            prefetch_related
        )

    if select_related and prefetch_related:
        return _get_queryset(manager.select_related(
            *select_related).prefetch_related(*prefetch_related))
    elif not select_related and prefetch_related:
        return _get_queryset(manager.prefetch_related(*prefetch_related))
    elif select_related and not prefetch_related:
        return _get_queryset(manager.select_related(*select_related))
    return _get_queryset(manager)
