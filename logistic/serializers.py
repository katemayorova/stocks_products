from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(**position, stock=stock)

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions', None)

        if 'address' in validated_data:
            instance = super().update(instance, validated_data)

        if positions is not None:
            StockProduct.objects.filter(stock=instance).delete()
            for position in positions:
                StockProduct.objects.create(**position, stock=instance)

        return instance

