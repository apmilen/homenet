import graphene
import rentals.schema


class Query(rentals.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
