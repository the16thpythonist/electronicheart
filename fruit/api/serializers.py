from rest_framework import serializers

from fruit.models import Fruit


class FruitDefaultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fruit
        fields = ["id", "name", "description"]


class FruitDetailSerializer(FruitDefaultSerializer):
    class Meta:
        model = FruitDefaultSerializer.Meta.model
        fields = FruitDefaultSerializer.Meta.fields + ["detail", "detail_link"]
