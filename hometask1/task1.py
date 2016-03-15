# -*- coding: utf-8 -*-
'''
1.
Предположим, что решающее правило >=0.5 – фрод, в остальных случаях – не фрод.
По указанной выборки рассчитать: true positive, false positive, true negative, false
negative для p1_fraud, p2_fraud, p3_fraud правил.
'''
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

if __name__ == '__main__':
    p = 0.5 # задали решающее правило
    data = pd.read_csv('2016.02.20.vyygrusska.csv', ';') # выгрузим данные из csv

    # найдем tp, fp, tn, fn для ЭС 1, 2, 3
    for i in xrange(1, 4):
        print 'p' + str(i) + '_Fraud System'

        print 'true positive rate'
        print tpr(data['p' + str(i) + '_Fraud'], data['CLASS'], p)

        print 'false positive rate'
        print fpr(data['p' + str(i) + '_Fraud'], data['CLASS'], p)

        print 'true negative rate'
        print tnr(data['p' + str(i) + '_Fraud'], data['CLASS'], p)

        print 'false negative rate'
        print fnr(data['p' + str(i) + '_Fraud'], data['CLASS'], p)

        print '-------------------------------------------'
