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
    def validate(self, data):
        produto_ids = self.initial_data.get('produtos', [])
        self.produtos = models.Produto.objects.filter(id__in=produto_ids)
        return super().validate(data)

    @transaction.atomic
    def create(self, validated_data):
        validated_data['comprador'] = self.context['request'].user
        validated_data['data'] = get_dia_util(timezone.now().date())
        validated_data['data_efetiva'] = timezone.now()
        compra = super().create(validated_data)

        itens = []
        for produto in self.produtos:
            itens.append(models.ItemCompra(
                compra=compra, produto=produto,
            ))
        models.ItemCompra.objects.bulk_create(itens)
        return compra

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
