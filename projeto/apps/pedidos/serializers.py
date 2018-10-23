from rest_framework import serializers
from django.utils import timezone
from . import models
from apps.core.utils import get_dia_util


class Produto(serializers.ModelSerializer):
    class Meta:
        model = models.Produto
        fields = ('pk', 'nome', 'valor')
        read_only = ('pk',)


class Compra(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['comprador'] = self.context['request'].user
        validated_data['data'] = timezone.now()
        validated_data['data_efetiva'] = timezone.now()
        return super().create(validated_data)

    class Meta:
        model = models.Compra
        fields = ('produtos',)
        read_only = ('pk', 'data', 'data_efetiva')
