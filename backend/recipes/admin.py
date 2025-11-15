from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import CharField, F, Q, Value
from django.db.models.functions import Concat
from django.utils.safestring import mark_safe

from .models import (FavoriteRecipes, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Subscriptions, Tag, User)


class RecipeIngredientInlineForm(forms.ModelForm):
    """
    Форма для редактирования ингредиентов рецепта во встроенном режиме.
    """

    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all().annotate(
            display_name=Concat(
                F('name'), Value(' ('), F('measurement_unit'), Value(')'),
                output_field=CharField()
            )
        ),
        label="Ингредиент",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].label_from_instance = (
            lambda ingredient: ingredient.display_name
        )

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    form = RecipeIngredientInlineForm
    extra = 1
    min_num = 1
    verbose_name = "Ингредиент"
    verbose_name_plural = "Ингредиенты"


class CookingTimeFilter(admin.SimpleListFilter):
    """
    Фильтр для админ-панели, позволяющий отсортировать рецепты.
    """
    title = 'Время готовки'
    parameter_name = 'cooking_time'

    def lookups(self, request, model_admin):
        all_recipes = model_admin.model.objects.all()
        all_cooking_times = all_recipes.values_list('cooking_time', flat=True)
        minimum_time = min(all_cooking_times) if all_cooking_times else 0
        maximum_time = max(all_cooking_times) if all_cooking_times else 0

        if maximum_time == 0:
            medium_threshold = 0
            long_threshold = 0
        else:
            interval = (maximum_time - minimum_time) / 3
            medium_threshold = minimum_time + interval
            long_threshold = medium_threshold + interval

        ranges = [
            ((0, medium_threshold), f'Быстро (< {int(medium_threshold)} мин)'),
            ((medium_threshold, long_threshold),
             f'Средне (от {int(medium_threshold)}'
             'до {int(long_threshold)} мин)'),
            ((long_threshold, maximum_time + 1),
             f'Долго (> {int(long_threshold)} мин)'),
        ]
        return ranges

    def queryset(self, request, queryset):
        cooking_time_ranges = request.GET.getlist('cooking_time')
        if not cooking_time_ranges:
            return queryset

        filters = Q()
        for cooking_time_range in cooking_time_ranges:
            try:
                start_time, end_time = map(int, cooking_time_range.split(','))
                filters |= Q(cooking_time__range=(start_time, end_time))
            except ValueError:
                pass

        return queryset.filter(filters)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'cooking_time', 'author',
        'get_tags', 'get_ingredients', 'get_image',
        'in_favorites'
    )
    list_filter = ('tags', 'author', CookingTimeFilter)
    inlines = (RecipeIngredientInline,)

    @admin.display(description='Теги')
    def get_tags(self, recipe):
        return mark_safe('<br>'.join(tag.name for tag in recipe.tags.all()))

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, recipe):
        return mark_safe('<br>'.join(
            f'{item.ingredient.name} '
            f'({item.ingredient.measurement_unit}) - {item.amount}'
            for item in recipe.recipe_ingredients.select_related('ingredient')
        ))

    @admin.display(description='Картинка')
    def get_image(self, recipe):
        return (
            mark_safe(f'<img src="{recipe.image.url}" '
                      f'style="max-width: 200px; max-height: 200px; " />')
            if recipe.image
            else ''
        )

    @admin.display(description='В избранном')
    def in_favorites(self, recipe):
        return recipe.favoriterecipes.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', 'recipes_count')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)

    @admin.display(description='Рецепты')
    def recipes_count(self, ingredient):
        return ingredient.recipes.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'recipes_count')
    search_fields = ('name', 'slug',)

    @admin.display(description='Рецепты')
    def recipes_count(self, tag):
        return tag.recipes.count()


@admin.register(ShoppingList, FavoriteRecipes)
class ShoppingListFavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'recipe__name',)
    list_filter = ('author', 'recipe',)


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_filter = ('user', 'author',)


@admin.register(User)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'full_name', 'email', 'avatar_display',
        'recipes_count', 'subscriptions_count', 'subscribers_count'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

    @admin.display(description='ФИО')
    def full_name(self, user):
        return f'{user.first_name} {user.last_name}'

    @admin.display(description='Аватар', ordering='avatar')
    def avatar_display(self, user):
        return mark_safe(
            f'<img src="{user.avatar.url}" '
            f'style="max-width: 50px; max-height: 50px; " />'
        ) if user.avatar else ''

    @admin.display(description='Рецепты')
    def recipes_count(self, user):
        return user.recipes.count()

    @admin.display(description='Подписки')
    def subscriptions_count(self, user):
        return user.authors.count()

    @admin.display(description='Подписчики')
    def subscribers_count(self, user):
        return user.followers.count()


admin.site.unregister(Group)
