from strawberry import Schema
from .users.index import user_query, user_mutation

schema = Schema(query=user_query, mutation=user_mutation)