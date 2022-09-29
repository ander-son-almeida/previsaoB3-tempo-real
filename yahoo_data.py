# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 23:03:33 2021

@author: Anderson Almeida
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


def lendo_acao(sigla_acao, periodo, intervalo):
    
    # selecionando a ação
    target_acao = yf.Ticker(sigla_acao)

    # intervalo
    acao = target_acao.history(period=periodo, interval=intervalo, actions = False)
    acao = pd.DataFrame(acao)
    acao.reset_index(inplace=True, drop=False)
    
    #convertendo volume pra float
    acao['Datetime'] = acao['Datetime'].astype(str)
    
    #retirando o :00-03:00 do dataframe
    acao['Datetime'] = acao.Datetime.str.replace(':00-03:00', '')
    
    #convertendo pra string
    acao['Datetime'] = acao['Datetime'].convert_dtypes()
    
    # formatando a data
    acao['Datetime'] = pd.to_datetime(acao['Datetime'], format='%Y-%m-%d %H:%M')
    
    return acao
    