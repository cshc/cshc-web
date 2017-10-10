from graphene_django.filter import DjangoFilterConnectionField
from graphql.utils.ast_to_dict import ast_to_dict


def collect_fields(node):
    non_fields = ["edges", "node"]
    fields = []
    for leaf in node:
        if leaf.get('kind', None) == "Field" and not leaf["name"]["value"] in non_fields:
            fields.append(leaf["name"]["value"])

        if leaf.get("selection_set", None):
            fields = fields + \
                collect_fields(leaf["selection_set"]["selections"])

    return fields


def get_fields(info):
    """Return a nested dict of the fields requested by a graphene resolver"""
    node = ast_to_dict(info.field_asts)

    return collect_fields(node)


def optimize(qs, info, field_map):
    fields = get_fields(info)
    print(fields)
    for field in fields:
        if field in field_map:
            field_name, opt = field_map[field]
            if opt == "prefetch":
                qs = qs.prefetch_related(field_name)
            else:
                qs = qs.select_related(field_name)

    return qs


class OptimizableFilterConnectionField(DjangoFilterConnectionField):

    @staticmethod
    def merge_querysets(default_queryset, queryset):
        # There could be the case where the default queryset (returned from
        # the filterclass)
        # and the resolver queryset have some limits on it.
        # We only would be able to apply one of those, but not both
        # at the same time.

        # See related PR: https://github.com/graphql-python/graphene-django
        # /pull/126

        assert not (
            default_queryset.query.low_mark and queryset.query.low_mark), (
                'Received two sliced querysets (low mark) in the connection, '
                'please slice only in one.'
        )
        assert not (
            default_queryset.query.high_mark and queryset.query.high_mark), (
                'Received two sliced querysets (high mark) in the connection, '
                'please slice only in one.'
        )
        low = default_queryset.query.low_mark or queryset.query.low_mark
        high = default_queryset.query.high_mark or queryset.query.high_mark
        default_queryset.query.clear_limits()
        # queryset = super(cls, cls).merge_querysets(default_queryset, queryset)
        queryset.query.set_limits(low, high)

        return queryset
