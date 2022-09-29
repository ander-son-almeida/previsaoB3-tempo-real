# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 21:49:05 2022

@author: Anderson Almeida
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from yahoo_data import *
import warnings
from sklearn.exceptions import ConvergenceWarning
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=ConvergenceWarning)
    
    
def previsao(acao, sigla_acao):
    
    # Médias móveis
    acao['media5'] = acao['Close'].rolling(5).mean() #media movel de 5 pontos
    acao['media21'] = acao['Close'].rolling(21).mean() #media movel de 21 pontos
    
    # Shift
    acao['Close'] = acao['Close'].shift(-1)
    
    # Removendo NaN
    acao.dropna(inplace=True)
    
    # configurações das linhas
    qtd_linhas = len(acao)
    qtd_linhas_treino = int(qtd_linhas*0.75)
    qtd_linhas_teste = qtd_linhas - 15
    qtd_linhas_validacao = qtd_linhas_treino - qtd_linhas_teste
    
    print('Linhas de treino = 0 até {} \n'
          'Linhas de teste = {} até {}\n'
          'Linhas de validação = {} até {}'.format(qtd_linhas_treino,
                                            qtd_linhas_treino, qtd_linhas_teste,
                                            qtd_linhas_teste, qtd_linhas))
    
    # resetando index do dataframe
    acao = acao.reset_index(drop=True)
    
    # Criando features e Labels 
    features = acao.drop(['Datetime', 'Close'], 1)
    labels = acao['Close']
    
    ###############################################################################
    # Machine Learning - Kbest
    features_list = ('Open', 'Volume', 'media5', 'media21')
    k_best_features = SelectKBest(k='all') # lendo todas as features
    k_best_features.fit_transform(features, labels) 
    
    # score para as melhores features
    k_best_features_scores = k_best_features.scores_ 
    raw_pairs = zip(features_list[1:], k_best_features_scores) 
    ordered_pairs = list(reversed(sorted(raw_pairs, key=lambda x: x[1]))) 
    
    k_best_features_final = dict(ordered_pairs[:15])
    best_features = k_best_features_final.keys()
    
    # selecionado as features
    features = acao.loc[:,['High','Low','Volume','media5']]
    
    # Normalizando os dados de entrada(features)
    scaler = MinMaxScaler().fit(features) 
    features_scale = scaler.transform(features)
    
    #separa os dados de treino teste e validação
    X_train = features_scale[:qtd_linhas_treino]
    X_test = features_scale[qtd_linhas_treino:qtd_linhas_teste]
    y_train = labels[:qtd_linhas_treino]
    y_test = labels[qtd_linhas_treino:qtd_linhas_teste]
    
    
    ###############################################################################
    #treinamento usando regressão linear
    lr = linear_model.LinearRegression()
    lr.fit(X_train, y_train)
    pred= lr.predict(X_test)
    cd1 =r2_score(y_test, pred)
    
    ###############################################################################
    #rede neural
    
    rn = MLPRegressor(max_iter=2000)
    rn.fit(X_train, y_train)
    pred = rn.predict(X_test)
    cd2 = rn.score(X_test, y_test)
    
    ###############################################################################
    
    print('coeficientes de determinação:')
    print('Regressão linear = ', np.around(cd1, decimals=2))
    print('Rede Neural = ', np.around(cd2, decimals=2))
    
    ###############################################################################
    # previsão
    
    previsao = features_scale[qtd_linhas_teste:qtd_linhas]
    data_pregao_full = acao['Datetime']
    data_pregao = data_pregao_full[qtd_linhas_teste:qtd_linhas]
    res_full = acao['Close']
    res = res_full[qtd_linhas_teste:qtd_linhas]
    pred = lr.predict(previsao)
    
    df = pd.DataFrame({'Datetime':data_pregao, 'real':res, 'previsao':pred})
    df['real'] = df['real'].shift(+1)
    df.set_index('Datetime', inplace=True)
    
    ###############################################################################
    #grafico
    plt.figure()
    plt.title('Predição: {}'.format(sigla_acao))
    plt.plot(df['real'], label = 'Real', marker = 'o')
    plt.plot(df['previsao'], label ='Previsão', marker = 'o')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento (R$)')
    plt.legend()