# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 23:27:11 2021

@author: Anderson Almeida
"""

from funcao_previsao import *

# definições 
sigla_acao = 'MGLU3.SA' #MGLU3.SA ITUB3.SA 
periodo = '1mo' # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
intervalo = '15m' # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

# lendo ação
acao = lendo_acao(sigla_acao, periodo, intervalo)

# executando a previsao
previsao(acao, sigla_acao)
