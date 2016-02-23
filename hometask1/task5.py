# -*- coding: utf-8 -*-
'''
5.
Создайте ансамбль в виде функции голосования при пороге каждого правила >=0.5,
>=0.8. Найдите необходимые пороги для каждого правила ЭС, чтобы false positive
ансамбля была минимальна.
'''
import pandas as pd

# F - fraud, G - not fraud

def es(data, p):
    '''
    Функция "переводит" решения ЭС в булево представление в соответствии с заданным порогом
    :param data: решения ЭС
    :param p: порог
    :param return: список решения ЭС в булевом представлении
    '''
    return [1 if x >= p else 0 for x in data]

def summ(systems, i):
    '''
    Суммирующая вспомогательная функция для мажритарной функции
    :param systems: решения ЭС
    :param i: номер решения ЭС
    :param return: сумма решений
    '''
    ans = 0
    for j in xrange(0, len(systems)):
        ans += systems[j][i]
    return ans

def funcMajority(systems):
    '''
    Мажоритарная функция
    :param systems: ЭС и их решения
    :param return: решение функции на основании решений ЭС
    '''
    return ['F' if int(0.5 + ((float(summ(systems, i)) - 0.5)/float(len(systems)))) == 1 else 'G' for i,x in enumerate(systems[0])]

def true_negativeR(data, check):
    '''
    Функция для нахождения true positive rate
    :param data: решения ЭС
    :param check: проверенные данные
    :param return: tpr
    '''
    tn = len([x for i,x in enumerate(data) if (check[i] == 'F' and data[i] == 'F')]) #tn
    fp = len([x for i,x in enumerate(data) if (check[i] == 'F' and data[i] == 'G')]) #fp
    return float(tn) / float(tn+fp)

def false_positiveR (data, check):
    '''
    Функция для нахождения false negative rate
    :param data: решения ЭС
    :param check: проверенные данные
    :param return: fnr
    '''
    return float(1) - true_negativeR(data, check)

if __name__ == '__main__':
    data = pd.read_csv('2016.02.20.vyygrusska.csv', ';') # выгрузим данные из csv

    p = 0.5 # задали решающее правило

    # мажоритарная функция для всех систем
    majority = funcMajority([es(data['p' + str(i) + '_Fraud'], p) for i in xrange(1, 4)])

    # false positive rate для ансамбля с мажоритарной функцией
    print false_positiveR(majority, data['CLASS'])

    print '----------------------'

    p = 0.8 # задали решающее правило

    # мажоритарная функция для всех систем
    majority = funcMajority([es(data['p' + str(i) + '_Fraud'], p) for i in xrange(1, 4)])

    # false positive rate для ансамбля с мажоритарной функцией
    print false_positiveR(majority, data['CLASS'])
