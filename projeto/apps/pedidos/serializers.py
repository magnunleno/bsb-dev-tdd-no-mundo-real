from rest_framework import serializers
from django.db.models import Sum
from django.utils import timezone
from . import models
from apps.core.utils import get_dia_util
from django.db import transaction


class ItemCompraSerializer(serializers.ModelSerializer):
    produto_pk = serializers.CharField(source="produto.pk")
    produto_valor = serializers.CharField(source="produto.valor")
    produto_nome = serializers.CharField(source="produto.nome")

    class Meta:
        model = models.ItemCompra
        fields = ('pk', 'produto_pk', 'produto_valor', 'produto_nome')
        read_only_fields = ('pk', 'produto_pk', 'produto_valor',
                            'produto_nome')


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Compra
        fields = ('pk', 'data', 'data_efetiva', 'produtos')
        read_only_fields = ('pk', 'data', 'data_efetiva')


class CompraReadOnlySerializer(serializers.ModelSerializer):
    itens_compra = ItemCompraSerializer(many=True)

    class Meta:
        model = models.Compra
        fields = ('pk', 'data', 'data_efetiva', 'itens_compra')
        read_only_fields = ('pk', 'data', 'data_efetiva', 'itens_compra')
