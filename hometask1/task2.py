"""
Задача 1.
1. Предположим, что решающее правило >=0.5 – фрод, в остальных случаях – не фрод.
По указанной выборки рассчитать: true positive, false positive, true negative, false
negative для всех правил
2. Для каждой ЭС найдите порог решающего правила, для которого false positive не
более 0.2
3. Найдите полноту и точность.
"""

import pandas as pd


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

def esNotWorked(data, check, kind, p):
    '''
    Функция рассчитывает, сколько раз экспертая система не сработала
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param kind: вид тразакции: F - фрод, G - легитимная транзакция
    :param p: значение решающего правила
    :param return: возвращает количество удовлетворяющих условию данных
    '''
    return len([c for d,c in zip(data, check) if (d < p and (c == kind))])

def rate (x, y):
    return float(x) / (float(x + y))

def tpr (data, check, p):
    '''
    true positive rate
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param p: значение решающего правила
    :param return: возвращает true positive rate
    '''
    return rate(esWorked(data, check, 'F', p), esNotWorked(data, check, 'F', p))

def tnr (data, check, p):
    '''
    true negative rate
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param p: значение решающего правила
    :param return: возвращает true negative rate
    '''
    return rate(esNotWorked(data, check, 'G', p), esWorked(data, check, 'G', p))

def fnr (data, check, p):
    '''
    false negative rate
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param p: значение решающего правила
    :param return: возвращает false negative rate
    '''
    return 1 - tpr(data, check, p)

def fpr (data, check, p):
    '''
    false positive rate
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param p: значение решающего правила
    :param return: возвращает false positive rate
    '''
    return 1 - tnr(data, check, p)


def searchThreshold(data, check, p):
    '''
    Функция находит такой порог для решающего правила, чтобы FPR <= P
    :param data: данные, определённые ЭС
    :param check: заведомо известные данные
    :param p: условие для FPR
    :param return: возвращает найденный порог
    '''
    x = 0
    y = 1
    jump = 0.01
    while (x < y):
        x += jump
        falsepositive = fpr(data, check, x)
        if falsepositive <= p:
            return x

def recall(tp, fn):
    '''
    Полнота
    :param tp: true positive
    :param fn: false negative
    :param return: recall
    '''
    return float(tp)/float(tp + fn)

def precision(tp, fp):
    '''
    Точность
    :param tp: true positive
    :param fp: false posotove
    :param return: precision
    '''
    return float(tp)/float(tp + fp)


if __name__ == '__main__':
    p = 0.5 # задали решающее правило

    falsepositive = 0.2 # порог false positive


    data = pd.read_csv('unloading.csv', ',') # выгрузим данные из csv

    # найдем tp, fp, tn, fn для ЭС 1, 2, 3, 4, 5
    for i in range(1, 6):
        print('p' + str(i) + '_Fraud System')
        column_name = 'p' + str(i) + '_Fraud'
        print('\ttrue positive rate')
        print('\t', tpr(data[column_name], data['CLASS'], p))

        print('\tfalse positive rate')
        print('\t', fpr(data[column_name], data['CLASS'], p))

        print('\ttrue negative rate')
        print('\t', tnr(data[column_name], data['CLASS'], p))

        print('\tfalse negative rate')
        print('\t', fnr(data[column_name], data['CLASS'], p))

        print('\tthreshold rule for false positive rate < 0.2')
        print('\t', searchThreshold(data[column_name], data['CLASS'], falsepositive))

        tp = esWorked(data[column_name], data['CLASS'], 'F', p)
        fn = esNotWorked(data[column_name], data['CLASS'], 'G', p)
        fp = esWorked(data[column_name], data['CLASS'], 'G', p)

        print('\trecall')
        print('\t', recall(tp, fn))

        print('\tprecision')
        print('\t', precision(tp, fp))

        print('\n\n')