"""
Задача 5
1. Зададим ансамбль через параметры A, B, C:
p =(A*p1_fraud+B*p2_fraud+C*p3_fraud)/(A+B+C).
Найдите A, B, C, чтобы индекс Джини ансамбля был бы максимальным. При каких A,
B, C индекс Джини минимален? Найдите A, B, C для максимального true positive при
условии, что false positive должен быть равен 0.1. Каков порог решающего правила?
"""

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
import itertools
from operator import itemgetter


def summ(systems, i, A, B, C, D, E):
    '''
    Суммирующая вспомогательная функция для мажритарной функции
    :param systems: решения ЭС
    :param i: номер решения ЭС
    :param A: параметр А
    :param B: параметр B
    :param C: параметр С
    :param return: сумма решений
    '''
    return A*systems[0][i] + B*systems[1][i] + C*systems[2][i] + D*systems[3][i] + E*systems[4][i]


def func(systems, A, B, C, D, E):
    return [float(summ(systems, i, A, B, C, D, E)) / float(A + B + C + D + E) for i in range(0, len(systems[0]))]


def getData(data, check):
    '''
    Функция определяет реальные и спрогнозированные вероятности
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param return: возвращает actual, predictions
    '''
    actual = list()
    predictions = list()
    for d,c in zip(data, check):
        if c != 'U':
            predictions.append(d)
            if c == 'F':
                actual.append(1)
            else:
                actual.append(0)

    return actual, predictions     


if __name__ == '__main__':
    data = pd.read_csv('unloading.csv', ',') # выгрузим данные из csv

    parametrs = itertools.permutations(list(range(1, 10)), 5)

    results = list()

    for param in parametrs:
        # функция p = (A*p1_fraud + B*p2_fraud + C*p3_fraud + D*p4_fraud + E*p5_fraud)/(A + B + C + D + E)
        P = func([data['p' + str(i) + '_Fraud'] for i in range(1, 6)], param[0], param[1], param[2], param[3], param[4])
        actual, predictions = getData(P, data['CLASS'])
        false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predictions)
        roc_auc = auc(false_positive_rate, true_positive_rate)

        results.append({
                 'Gini': ((roc_auc * 2) - 1),
                 'parametrs': [param[0], param[1], param[2], param[3], param[4]],
                 'fpr': false_positive_rate,
                 'tpr': true_positive_rate,
                 'thresholds': thresholds

        })

    # найдем максимальный индекс Джини
    Gini = sorted(results, key=itemgetter('Gini'))
    print('max Gini:', Gini[-1]['Gini'], 'params:', Gini[-1]['parametrs'])
    print('min Gini:', Gini[0]['Gini'],'params:', Gini[0]['parametrs'])
