# -*- coding: utf-8 -*-
'''
10. Предположим, что при верной сработке мы “спасаем” деньги клиентов, равные
AMOUNT (это «репутационную прибыль» банка). При сработке клиента блокируют.
Заблокированный клиент звонит в 90% случаев в контактный центр. Цена разговора с
клиентом 40 рублей. Если клиента несправедливо заблокировали, то банк терпит
«репутационные издержки», оцененные в 3000 рублей. Рассчитайте максимальный
CBA для одного из pi_fraud.
'''
import pandas as pd
import numpy as np
from task1 import esWorked

# посчитать количество обнаруженного фрода
# посчитать количество издержек за звонки

def callsCosts(data, p):
    '''
    Функция рассчитывает затраты на звонки от клиентов
    :param data: данные ЭС
    :param p: порог
    :param return: стоимость звонков
    '''
    fraud_count = len([x for x in data if (x >= p)])
    call_count = fraud_count * 0.9
    cost_of_calls = call_count * 40
    return cost_of_calls

# посчитать репутационные издержки за ошибку fp (ложное срабатывание ЭС)

def lossReputation(data, check, p):
    '''
    Функция считает репутационные издержки
    :param data: данные ЭС
    :param check: фрод/не фрод
    :param p: порог
    :param return: репутационные издержки
    '''
    fp = esWorked(data, check, 'G', p) # кол-во ошибок 1 рода
    reputation_loss = fp * 3000
    return reputation_loss

# посчитать репутационную прибыль банка в случае верно обнаруженного фрода

def costsReputation(data, check, amount, p):
    '''
    Функция считает репутационную прибыль
    :param data: данные ЭС
    :param check: фрод/не фрод
    :param amount: стоимость операций
    :param p: порог
    :param return: репутационная прибыль
    '''
    reputation_costs = 0
    for d,c,a in zip(data, check, amount):
        if d >= p and c == 'F':
            # какая-то дичь с NaN
            if not np.isnan(float(a)):
                reputation_costs += float(a)

    return reputation_costs

# а что, при пропуске фрода (fn ошибка 2 рода) банк не теряет ничего? Сбербанк, наверное, какой-нибудь

if __name__ == '__main__':
    data = pd.read_csv('2016.02.20.vyygrusska.csv', ';')
    for i in xrange(1, 4):
        buf = [0, 0]
        x = 0
        y = 1
        jump = 0.01
        while x < y:
            x += jump
            p = x

            cost_of_calls = callsCosts(data['p' + str(i) + '_Fraud'], p)
            reputation_loss = lossReputation(data['p' + str(i) + '_Fraud'], data['CLASS'], p)
            reputation_costs = costsReputation(data['p' + str(i) + '_Fraud'], data['CLASS'], data['AMOUNT'], p)
            CBA = reputation_costs - reputation_loss - cost_of_calls

            if buf[1] < CBA:
                buf = [p, CBA]
        print 'наибольший CBA для ЭС p' + str(i) + '_Fraud при p =', buf[0], ', CBA =', buf[1], 'рублей'
        print '----------------------------'
