from django.urls import path

from src.cookbook.apps import CookbookConfig
from src.cookbook.views import (
    add_product_to_recipe,
    cook_recipe,
    show_recipes_without_product
)

app_name = CookbookConfig.name

urlpatterns = [
    path(
        'add_product_to_recipe/',
        add_product_to_recipe,
        name='add_product_to_recipe',
    ),
    path(
        'cook_recipe/',
        cook_recipe,
        name='cook_recipe',
    ),
    path(
        'show_recipes_without_product/',
        show_recipes_without_product,
        name='show_recipes_without_product',
    ),
]
