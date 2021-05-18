from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql.execution.base import ResolveInfo

from ingredients.models import Category, Ingredient


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info: ResolveInfo):
        return queryset


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info: ResolveInfo):
        return queryset


class Query(ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)
    """
    query {
      allIngredients {
        edges {
          node {
            id,
            name
          }
        }
      }
    }
    """

    ingredient = relay.Node.Field(IngredientNode)
    """
    query {
      ingredient(id: "SW5ncmVkaWVudE5vZGU6MQ==") { # base64 解码之后：IngredientNode:1
        name
      }
    }
    """
    all_ingredients = DjangoFilterConnectionField(IngredientNode)
    """
    query {
      allIngredients {
        edges {
          node {
            id,
            name
          }
        }
      }
    }
    
    query {
      # You can also use `category: "CATEGORY GLOBAL ID"`
      allIngredients(name_Icontains: "e", category_Name: "Meat") {
        edges {
          node {
            name
          }
        }
      }
    }
    """