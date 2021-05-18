from django.http.request import HttpRequest
import graphene
from graphene_django import DjangoObjectType
from graphql.execution.base import ResolveInfo

from ingredients.models import Category, Ingredient
import ingredients.schema


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(ingredients.schema.Query, graphene.ObjectType):
    all_ingredients_v1 = graphene.List(IngredientType)
    category_by_name_v1 = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients_v1(root, info: ResolveInfo):
        """
        query {
          allIngredientsV1 {
            id
            name
          }
        }
        """
        context: HttpRequest = info.context
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name_v1(root, info, name):
        """
        query {
          categoryByNameV1(name: "Dairy") {
            id
            name
            ingredients {
              id
              name
            }
          }
        }
        """
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
