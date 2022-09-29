# Sobre

Neste repositório temos um modelo simples de previsão em tempo real dos ativos da B3 usando modelos de regressão linear e redes neurais da biblioteca scikit-learn. Esse trabalho foi inspirado no código do Fabrício Mattos, disponível [neste link](https://github.com/fabrimatt/machine_learnig/blob/master/Previs%C3%A3o%20pre%C3%A7o%20a%C3%A7%C3%B5es.ipynb).

A implementação realizada foi a criação de um dataset, com períodos de 15 minutos, utilizando a biblioteca yahoo finance para alimentar o modelo de previsão rapidamente. Ressalta-se que existe um delay nas consultas realizadas com yahoo finance de 15 minutos ou mais.

### Importante

Esse programa tem como finalidade o estudo de modelos em machine learning e não deve ser usado para tomada de decisões no mercado financeiro.
