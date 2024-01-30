from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    times_used = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-name', ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField(Product, through='RecipeProduct')

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('recipe', 'product')
