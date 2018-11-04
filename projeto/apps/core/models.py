#!/usr/bin/env python3
# encoding: utf-8

from django.db import models


class Feriado(models.Model):
    dia = models.DateField(primary_key=True)
    descricao = models.CharField(max_length=200)
