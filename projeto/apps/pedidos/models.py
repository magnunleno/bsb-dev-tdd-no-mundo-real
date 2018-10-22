from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Produto(models.Model):
    nome = models.CharField(max_length=500)
    valor = models.DecimalField(max_digits=19, decimal_places=2)


class Compra(models.Model):
    data = models.DateField()
    data_efetiva = models.DateTimeField(auto_now_add=True)
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    produtos = models.ManyToManyField(
        Produto,
        through='ItemCompra',
        through_fields=('compra', 'produto'),
    )


class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
