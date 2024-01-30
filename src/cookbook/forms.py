from django import forms


class AddProductToRecipeForm(forms.Form):
    recipe_id = forms.IntegerField(required=True, min_value=1)
    product_id = forms.IntegerField(required=True, min_value=1)
    weight = forms.IntegerField(required=True, min_value=1)

    class AddProductToRecipeDTO:
        def __init__(self, recipe_id, product_id, weight):
            self.recipe_id = recipe_id
            self.product_id = product_id
            self.weight = weight

    def to_dto(self) -> AddProductToRecipeDTO:
        return self.AddProductToRecipeDTO(
            recipe_id=self.cleaned_data['recipe_id'],
            product_id=self.cleaned_data['product_id'],
            weight=self.cleaned_data['weight'],
        )


class RecipeForm(forms.Form):
    recipe_id = forms.IntegerField(required=True, min_value=1)

    def get_recipe_id(self) -> int:
        return self.cleaned_data['recipe_id']


class ProductForm(forms.Form):
    product_id = forms.IntegerField(required=True, min_value=1)

    def get_product_id(self) -> int:
        return self.cleaned_data['product_id']
