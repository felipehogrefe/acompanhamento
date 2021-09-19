from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
import os, time
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acompanhamento.settings')
django.setup()

from investimentos.models import criar_nova_acao

with open('lista_acoes_br.txt', 'r') as nome_acoes:
    for linha in nome_acoes.readlines():
        print(linha.replace('\n',''))
        criar_nova_acao(linha.replace('\n',''))
        time.sleep(12)




# key = 'P8Z69S2VPW8P5CUF'
#
# ts = TimeSeries(key=key, output_format='pandas')
#
# gl = ts.get_symbol_search('GOGL34.SAO')
#
# dados, meta_dados = ts.get_daily(symbol='GOGL34.SAO', outputsize='full')
#
# # print(dados)
#
# dados['4. close'].plot()
#
