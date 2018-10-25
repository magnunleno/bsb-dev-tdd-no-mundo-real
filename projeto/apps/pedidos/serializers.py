from rest_framework import serializers
from django.db.models import Sum
from django.utils import timezone
from . import models
from apps.core.utils import get_dia_util
from django.db import transaction


class ItemCompraSerializer(serializers.ModelSerializer):
    pk_produto = serializers.SerializerMethodField()
    nome_produto = serializers.SerializerMethodField()

    def get_pk_produto(self, obj):
        return obj.produto.pk

    def get_nome_produto(self, obj):
        return obj.produto.nome

    class Meta:
        model = models.ItemCompra
        fields = ('pk', 'valor', 'pk_produto', 'nome_produto')
        read_only_fields = ('pk', 'valor', 'pk_produto', 'nome_produto')


class CompraSerializer(serializers.ModelSerializer):
    def validate(self, data):
        produto_ids = self.initial_data.get('produtos', [])
        self.produtos = models.Produto.objects.filter(id__in=produto_ids)
        if len(produto_ids) != self.produtos.count():
            raise serializers.ValidationError({
                'produtos': 'Não foi possível encontrar um ou mais produtos'
            })
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
                compra=compra, produto=produto, valor=produto.valor,
            ))
        models.ItemCompra.objects.bulk_create(itens)
        return compra

    class Meta:
        model = models.Compra
        fields = ('pk', 'data', 'data_efetiva', 'produtos')
        read_only_fields = ('pk', 'data', 'data_efetiva')


class CompraReadOnlySerializer(serializers.ModelSerializer):
    itens_compra = ItemCompraSerializer(many=True)
    valor_total = serializers.SerializerMethodField()

    def get_valor_total(self, obj):
        return obj.itens_compra.aggregate(total=Sum('valor'))['total']

    class Meta:
        model = models.Compra
        fields = ('pk', 'data', 'data_efetiva', 'itens_compra', 'valor_total')
        read_only_fields = ('pk', 'data', 'data_efetiva', 'itens_compra',
                            'valor_total')
