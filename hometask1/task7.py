"""
Задача 7.
Предположим, что при верной сработки мы “спасаем” деньги клиентов, равные
AMOUNT_RUB. При сработке клиента блокируют. Заблокированный клиент звонит в 90%
случаев в контактный центр. Цена разговора с клиентом 400 рублей. Если клиента несправедливо заблокировали, то банк терпит “репутационные издержки”, оцененные в 2000
рублей. Постройте уравнение для расчета CBA. Решите это уравнение.
"""


import pandas as pd
import numpy as np
from operator import itemgetter

# посчитать количество обнаруженного фрода
# посчитать количество издержек за звонки

def esWorked(data, check, kind, p):
    '''
    Функция рассчитывает, сколько раз экспертая система сработала
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param kind: вид тразакции: F - фрод, G - легитимная транзакция
    :param p: значение решающего правила
    :param return: возвращает количество удовлетворяющих условию данных
    '''
    return len([c for d,c in zip(data, check) if (d >= p and (c == kind))])


def callsCosts(data, p):
    '''
    Функция рассчитывает затраты на звонки от клиентов
    :param data: данные ЭС
    :param p: порог
    :param return: стоимость звонков
    '''
    fraud_count = len([x for x in data if (x >= p)])
    call_count = fraud_count * 0.9
    cost_of_calls = call_count * 400
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
    reputation_loss = fp * 2000
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


def max_CBA(data, pi_num):
    p = 0.1
    CBAs = list()

    while p < 1:
        p += 0.1

        column_name = 'p' + str(pi_num) + '_Fraud'

        cost_of_calls = callsCosts(data[column_name], p)
        reputation_loss = lossReputation(data[column_name], data['CLASS'], p)
        reputation_costs = costsReputation(data[column_name], data['CLASS'], data['AMOUNT'], p)
        CBA = reputation_costs - reputation_loss - cost_of_calls

        CBAs.append({
                    'CBA': CBA,
                    'pi': 'p' + str(pi_num),
                    'p': p
            })
    CBAs = sorted(CBAs, key=itemgetter('CBA'))
    return CBAs[-1]

# а что, при пропуске фрода (fn ошибка 2 рода) банк не теряет ничего? Сбербанк, наверное, какой-нибудь

if __name__ == '__main__':
    data = pd.read_csv('unloading.csv', ',')
    for i in range(1, 6):
        result = max_CBA(data, i)

        print('p' + str(i) + '_fraud max CBA:', result['CBA'], 'with p =', result['p'])
