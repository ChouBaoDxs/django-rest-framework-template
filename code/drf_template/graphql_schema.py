from django.http.request import HttpRequest
import graphene
from graphene_django import DjangoObjectType
from graphql.execution.base import ResolveInfo

from ingredients.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info: ResolveInfo):
        """
        query {
          allIngredients {
            id
            name
          }
        }
        """
        context: HttpRequest = info.context
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()


    def resolve_category_by_name(root, info, name):
        """
        query {
          categoryByName(name: "Dairy") {
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