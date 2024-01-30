from http import HTTPStatus

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from src.cookbook.forms import AddProductToRecipeForm, RecipeForm, ProductForm
from src.cookbook.models import Recipe, RecipeProduct, Product


def _method_not_allowed():
    return JsonResponse(
        {'error': 'Method not allowed'},
        status=HTTPStatus.METHOD_NOT_ALLOWED
    )


def _validation_error(form):
    errors = form.errors
    return JsonResponse(
        {'error': errors},
        status=HTTPStatus.BAD_REQUEST
    )


def _success_response():
    return JsonResponse({"success": True})


def add_product_to_recipe(request):
    if request.method != 'GET':
        return _method_not_allowed()

    form = AddProductToRecipeForm(request.GET)
    if not form.is_valid():
        return _validation_error(form)

    dto = form.to_dto()

    with transaction.atomic():
        # Блокировка рецепта для синхронизации доступа к его данным
        recipe = Recipe.objects.select_for_update().get(id=dto.recipe_id)
        product = Product.objects.get(id=dto.product_id)

        # Попытка создать или обновить RecipeProduct
        recipe_product, created = RecipeProduct.objects.get_or_create(
            recipe=recipe,
            product=product,
            defaults={'weight': dto.weight}
        )

        if not created:
            # Если RecipeProduct уже существует, обновляем его вес
            recipe_product.weight = dto.weight
            recipe_product.save()
    return _success_response()


def cook_recipe(request):
    if request.method != 'GET':
        return _method_not_allowed()

    form = RecipeForm(request.GET)
    if not form.is_valid():
        return _validation_error(form)

    recipe_id = form.get_recipe_id()

    with transaction.atomic():
        # Получение ID продуктов, используемых в рецепте
        product_ids = RecipeProduct.objects.filter(
            recipe_id=recipe_id
        ).values_list('product_id', flat=True)

        # Блокировка продуктов одним запросом для
        # синхронизации доступа к их данным и избежания deadlock-а
        products = Product.objects.filter(
            id__in=product_ids
        ).select_for_update()

        # Увеличение счетчика использования для каждого продукта
        for product in products:
            product.times_used += 1
            product.save()
    return _success_response()


def show_recipes_without_product(request):
    if request.method != 'GET':
        return _method_not_allowed()

    form = ProductForm(request.GET)
    if not form.is_valid():
        return _validation_error(form)

    product_id = form.get_product_id()

    recipes = Recipe.objects.raw("""
        SELECT r.id, r.name FROM cookbook_recipe r
        LEFT JOIN cookbook_recipeproduct rp
        ON rp.recipe_id = r.id AND rp.product_id = %s
        WHERE rp.weight IS NULL OR rp.weight < %s
        """, [product_id, 10])

    context = {
        'recipes': recipes
    }
    return render(request, 'cookbook/recipes_table.html', context)
