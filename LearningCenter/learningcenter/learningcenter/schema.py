import graphene

from courses.schema import (
    Query as CoursesQuery,
    Mutation as CoursesMutation
)


class Query(CoursesQuery, graphene.ObjectType):
    pass


class Mutation(CoursesMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
