import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType, ObjectType
from my_app.models import TodoList, TodoItem

# Create a GraphQL type for the actor model


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

# Create a GraphQL type for the movie model


class TodoListType(DjangoObjectType):
    class Meta:
        model = TodoList


class TodoItemType(DjangoObjectType):
    class Meta:
        model = TodoItem


# Create a Query type
class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    todo_list = graphene.List(TodoListType, id=graphene.Int())
    todo_item = graphene.Field(TodoItemType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return get_user_model().objects.get(pk=id)

        return None

    def resolve_todo(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return TodoList.objects.get(pk=id)

        return None

    def resolve_todo_list(self, info, **kwargs):
        return TodoList.objects.all()

    # def resolve_movies(self, info, **kwargs):
    #     return Movie.objects.all()

# Create Input Object Types


# class UserInput(graphene.InputObjectType):
#     id = graphene.ID()
#     name = graphene.String()
#     password = graphene.String()


class TodoInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    # user = graphene.String()
    complete = graphene.Boolean()


class TodoItemInput(graphene.InputObjectType):
    id = graphene.ID()
    item_name = graphene.String()
    todo_list = graphene.ID(TodoInput)
    complete = graphene.Boolean()


# Create mutations for Users


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, username, password, email):
        ok = True
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(ok=ok, user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, id, username, password, email):
        ok = False
        user_instance = get_user_model().objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.username = username
            user_instance.email = email
            user_instance.set_password(password)
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class CreateTodo(graphene.Mutation):
    class Arguments:
        input = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(TodoListType)

    @login_required
    def mutate(self, info, input=None):
        ok = True
        user = info.context.user
        print(user)
        todo_instance = TodoList(
            title=input.title,
            user=user
        )
        todo_instance.save()
        return CreateTodo(ok=ok, todo=todo_instance)


# class UpdateTodo(graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         input = TodoInput(required=True)

#     ok = graphene.Boolean()
#     todo = graphene.Field(TodoListType)

#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         todo_instance = TodoList.objects.get(pk=id)
#         if todo_instance:
#             ok = True
#             # actors = []
#             # for actor_input in input.actors:
#             #     actor = Actor.objects.get(pk=actor_input.id)
#             #     if actor is None:
#             #         return UpdateMovie(ok=False, movie=None)
#             #     actors.append(actor)
#             todo_instance.title = input.title
#             todo_instance.user = input.user
#             todo_instance.complete = input.complete
#             todo_instance.save()
#             return UpdateTodo(ok=ok, todo=todo_instance)
#         return UpdateTodo(ok=ok, todo=None)


# create the Mutation type To complete our mutations

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    # update_user = UpdateUser.Field()
    create_todo = CreateTodo.Field()
    # update_todo = UpdateTodo.Field()


# map the queries and mutations to our application's API.
# schema = graphene.Schema(query=Query, mutation=Mutation)
