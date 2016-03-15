# -*- coding: utf-8 -*-
'''
7.
Зададим ансамбль через параметры A, B, C: p =(A*p1_fraud+B*p2_fraud+C*p3_fraud)/
(A+B+C). Найдите A, B, C, чтобы индекс Джини ансамбля был бы максимальным.
При каких A, B, C индекс Джини минимален? Найдите A, B, C для максимального true
positive при условии, что false positive должен быть равен 0.1. Каков порог решающего
правила?
'''
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from task3_4 import getData

def summ(systems, i, A, B, C):
    '''
    Суммирующая вспомогательная функция для мажритарной функции
    :param systems: решения ЭС
    :param i: номер решения ЭС
    :param A: параметр А
    :param B: параметр B
    :param C: параметр С
    :param return: сумма решений
    '''
    return A*systems[0][i] + B*systems[1][i] + C*systems[2][i]


def func(systems, A, B, C):
    return [float(summ(systems, i, A, B, C)) / float(A + B + C) for i in xrange(0, len(systems[0]))]

if __name__ == '__main__':
    data = pd.read_csv('2016.02.20.vyygrusska.csv', ';') # выгрузим данные из csv
    parametrs = list()

    for i in xrange(0, 3):
        parametrs.append([i for i in xrange(1, 10)])

    for i,x in enumerate(parametrs):
        A = x[i]

        for j in xrange(0, len(x)):
            B = x[j]

            for m in xrange(0, len(x)):
                C = x[m]

                # функция p = (A*p1_fraud + B*p2_fraud + C*p3_fraud)/(A + B + C)
                P = func([data['p' + str(i) + '_Fraud'] for i in xrange(1, 4)], A, B, C)

                actual, predictions = getData(P, data['CLASS'])
                false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predictions)
                roc_auc = auc(false_positive_rate, true_positive_rate)

                print 'A B C'
                print A, B, C
                print 'Gini:', (roc_auc * 2) - 1

                print '-----------------------------------'
