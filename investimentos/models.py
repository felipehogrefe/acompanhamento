import random

from django.contrib.auth.models import User
from django.db import models
import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime

KEY_VALOR_ABERTURA = '1. open'
KEY_VALOR_FECHAMENTO = '4. close'
KEY_VOLUME = '5. volume'


class Acao(models.Model):
    sigla = models.CharField(max_length=6, unique=True)
    sigla_corrigida = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.sigla}"


class ValorAcao(models.Model):
    acao = models.ForeignKey(Acao, on_delete=models.CASCADE)
    data_referencia = models.DateField(null=False)
    valor_abertura = models.FloatField(null=False)
    valor_fechamento = models.FloatField(null=False)
    volume = models.FloatField(null=False)


class UsuarioAcao(models.Model):
    acao = models.ForeignKey(Acao, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_adicao = models.DateField(null=False)
    data_atualizacao = models.DateField(null=False)
    data_inicio_acompanhamento = models.DateField(null=False)

    def __str__(self):
        return f"{self.user.username} - {self.acao}"


def recuperar_acao(usuario, sigla_acao):
    acao = busca_acao(sigla_acao)
    if acao:
        usuario_acao = UsuarioAcao.objects.create(
            user=usuario,
            acao=acao,
            data_adicao=datetime.now(),
            data_atualizacao=datetime.now(),
            data_inicio_acompanhamento=datetime.now(),
        )
        return usuario_acao
    return None


def busca_acao(sigla_acao):
    qr_acao = Acao.objects.filter(sigla=sigla_acao)
    acao = qr_acao[0] if qr_acao[0] else criar_nova_acao(sigla_acao)
    atualizar_historico_acao(acao)

    return acao


def construir_time_series():
    key = random.choice(os.environ.get('API_KEY').split('-'))
    ts = TimeSeries(key=key, output_format='pandas')
    return ts


def criar_nova_acao(sigla_acao):
    ts = construir_time_series()
    result = ts.get_symbol_search(sigla_acao)[0]
    if len(result) > 0:
        sigla_corrigida = result['1. symbol'][[0]][0]

        acao = Acao.objects.get_or_create(
            sigla=sigla_acao,
            sigla_corrigida=sigla_corrigida
        )
        return acao
    return None


def atualizar_historico_acao(acao):
    if ValorAcao.objects.filter(acao=acao).count() == 0:
        criar_historico_acao(acao)


def criar_historico_acao(acao):
    ts = construir_time_series()
    dados, meta_dados = ts.get_daily(symbol=acao.sigla_corrigida, outputsize='full')
    for index, row in dados.iterrows():
        ValorAcao.objects.create(
            acao=acao,
            data_referencia=index,
            valor_abertura=row[KEY_VALOR_ABERTURA],
            valor_fechamento=row[KEY_VALOR_FECHAMENTO],
            volume=row[KEY_VOLUME],
        )
