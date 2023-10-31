"""
Serializers for Recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """serialzer for recipes"""

    class Meta:
        model = Recipe
        fields = ['id','title','time_minutes','price','link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serliazer for recipe details"""
    
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']