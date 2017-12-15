"""
Copied from https://gist.github.com/mjtamlyn/e8e03d78764552289ea4e2155c554deb
"""

from graphql.language.ast import (
    FragmentSpread, InlineFragment, ListValue, Variable,
)


def simplify_argument(arg):
    if isinstance(arg, ListValue):
        return [simplify_argument(a) for a in arg.values]
    if isinstance(arg, Variable):
        return arg.name.value
    return arg.value


def merge_dicts(d1, d2):
    for key in d2:
        if key in d1 and isinstance(d1[key], dict) and isinstance(d2[key], dict):
            merge_dicts(d1[key], d2[key])
        else:
            d1[key] = d2[key]


def get_fields(asts, resolve_info):
    fields = {}

    for field in asts:

        if isinstance(field, FragmentSpread):
            local = get_fields(
                resolve_info.fragments[field.name.value].selection_set.selections, resolve_info)
            for key in local:
                if key in fields and local[key].get('fields'):
                    try:
                        fields[key]['fields'].update(local[key]['fields'])
                    except KeyError:
                        fields[key].update(local[key])
                else:
                    fields[key] = local[key]

        elif isinstance(field, InlineFragment):
            local = get_fields(field.selection_set.selections, resolve_info)
            for key in local:
                if key in fields and local[key].get('fields'):
                    try:
                        fields[key]['fields'].update(local[key]['fields'])
                    except KeyError:
                        fields[key].update(local[key])
                else:
                    fields[key] = local[key]

        elif hasattr(field, 'selection_set'):
            local = {}
            if field.selection_set:
                local['fields'] = get_fields(
                    field.selection_set.selections, resolve_info)
            if field.arguments:
                local['arguments'] = {arg.name.value: simplify_argument(
                    arg.value) for arg in field.arguments}

            if fields.get(field.name.value):
                if local.get('fields'):
                    try:
                        merge_dicts(fields[field.name.value]
                                    ['fields'], local['fields'])
                    except KeyError:
                        fields[field.name.value]['fields'] = local['fields']
                if local.get('arguments'):
                    try:
                        fields[field.name.value]['arguments'].update(
                            local['arguments'])
                    except KeyError:
                        fields[field.name.value]['arguments'] = local['arguments']
            else:
                fields[field.name.value] = local

    return fields


def get_node_type(field):
    # Nullable foreign key fields are accessed directly from the
    # field.get_type().type property
    try:
        if hasattr(field.get_type().type._meta, 'model'):
            return field.get_type().type
    except:
        pass
    # Non-nullable foreign keys are wrapped in a 'NonNull' object with an 'of_type' property
    try:
        return field.get_type().type.of_type
    except AttributeError:
        try:
            if hasattr(field.type._meta, 'django_fields'):
                return field.type
        except AttributeError:
            pass
    return
