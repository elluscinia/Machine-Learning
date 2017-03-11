"""
Задача 6.
1. Постройте зависимость точности от pi_fraud для i от 1 до 3 для каждого дня.
2. Аналогично п.1 постройте зависимость полноты от pi_fraud.
3. Найдите SSI
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import datetime
import matplotlib.dates as mdates
import math

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

def get_precision(data, start, end, pi_num, p):
    column_name = 'p' + str(pi_num) + '_Fraud'
    tp = esWorked(data[column_name][start:end], data['CLASS'][start:end], 'F', p)
    fp = esWorked(data[column_name][start:end], data['CLASS'][start:end], 'G', p)

    try:
        return precision(tp, fp)
    except ZeroDivisionError as e:
        return 0

def get_recall(data, start, end, pi_num, p):
    column_name = 'p' + str(pi_num) + '_Fraud'
    tp = esWorked(data[column_name][start:end], data['CLASS'][start:end], 'F', p)
    fn = esNotWorked(data[column_name][start:end], data['CLASS'][start:end], 'G', p)

    try:
        return recall(tp, fn)
    except ZeroDivisionError as e:
        return 0


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def drawGraphsPeriod(x, y, pi_num, ps, graph_title):
    '''
    Функция рисует кривую Точность-Полнота за период
    :param x: дни
    :param y: значения
    :param pi_num: номер pi_fraud
    :param ps: значение решающего правила для каждого полученного набора значений
    :param graph_title: название отображаемого параметра
    :param return: ничего не возвращает
    '''
    plt.figure()


    for i,ps_i in enumerate(ps):
        plt.plot(x, list(y_i[i] for y_i in y), label='p=' + str(ps[i]))


    plt.title(graph_title + ' for p' + str(pi_num) + '_fraud per day')
    plt.legend(loc='lower right', fontsize='small')
    plt.grid(True, linestyle='-', color='0.75')
    plt.ylim([0.0, 1.0])
    plt.xlabel('Days')
    plt.ylabel(graph_title)
    plt.savefig(graph_title + '_p' + str(pi_num) + '_fraud_per_day.png')


def drawGraphsPerDay(data, begin, end):
    '''
    Функция рисует кривую в зависимости от дня
    :param data: данные ЭС
    :param begin: начало периода
    :param end: конец периода
    :param return: ничего не возвращает
    '''

    date = begin
    stop = end
    ps = list(frange(0.5, 0.9, 0.1))
    for i in range(1, 6):
        date = begin
        
        precisions = list()
        recalls = list()
        days = list()
        while (date < stop):
            start = data['EVENT_TIME'].searchsorted(str(date))[0]
            date += datetime.timedelta(days=1)
            end = data['EVENT_TIME'].searchsorted(str(date))[0]

            days.append(date)
            
            precisions_p = list()
            recalls_p = list()


            for p in ps:
                precisions_p.append(get_precision(data, start, end, i, p))
                recalls_p.append(get_recall(data, start, end, i, p))

            precisions.append(precisions_p)
            recalls.append(recalls_p)

        
        drawGraphsPeriod(days, precisions, i, ps, 'Precision')
        drawGraphsPeriod(days, recalls, i, ps, 'Recall')


if __name__ == '__main__':
    data = pd.read_csv('unloading.csv', ',')

    drawGraphsPerDay(data, datetime.datetime(2015,12,15,0,0,0), datetime.datetime(2016,1,13,0,0,0))
