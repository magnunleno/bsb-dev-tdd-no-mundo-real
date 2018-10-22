from rest_framework import serializers
from . import models


class Produto(serializers.ModelSerializer):
    class Meta:
        model = models.Produto
        fields = ('nome', 'valor')


class Compra(serializers.ModelSerializer):
    class Meta:
        model = models.Compra
        fields = ('data', 'data_efetiva', 'produtos')
