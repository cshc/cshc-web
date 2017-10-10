"""
Root GraphQL Schema for CSHC data
"""

import graphene
from graphene_django.debug import DjangoDebug
import competitions.schema
import venues.schema
import awards.schema
import members.schema
import teams.schema
import core.schema
import opposition.schema
import training.schema
import matches.schema


class Query(awards.schema.Query,
            venues.schema.Query,
            competitions.schema.Query,
            members.schema.Query,
            teams.schema.Query,
            core.schema.Query,
            opposition.schema.Query,
            training.schema.Query,
            matches.schema.Query,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query)
