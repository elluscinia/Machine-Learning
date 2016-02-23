# -*- coding: utf-8 -*-
'''
8.
Постройте зависимость точности и полноты от порога для pi_fraud для i от 1 до 3 для
каждого дня. Напишите функцию расчета SSI, принимающую на вход i, и время.
Рассчитайте SSI между двумя соседними неделями для промежутков от 15.12.2015 до
12.01.2016. Когда SSI максимальный, а когда минимальный? В качестве «окна»
выберете не неделю, а 4 дня, 2 дня, один день. Что можно сказать про SSI?
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc, precision_recall_curve
from task3_4 import getData
import datetime

def drawGraphsPeriod(data, start, end, date):
    '''
    Функция рисует кривую Точность-Полнота за период
    :param data: данные ЭС
    :param start: начало среда
    :param end: конец среза
    :param date: дата
    :param return: ничего не возвращает
    '''
    plt.clf()

    for i in xrange(3, 4):
        actual, predictions = getData(list(data['p' + str(i) + '_Fraud'][start:end]), list(data['CLASS'][start:end]))

        precision, recall, thresholds = precision_recall_curve(actual, predictions)

        plt.plot(recall, precision, label='%s PRC' % ('p' + str(i) + '_Fraud'))

    plt.title('Precision-recall curve for ' + str((date - datetime.timedelta(days=1)).strftime('%Y/%m/%d')))
    plt.legend(loc='lower right', fontsize='small')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.0])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.show()

def drawGraphsPerDay(data, begin, end):
    '''
    Функция рисует кривую Точность-Полнота за 1 день
    :param data: данные ЭС
    :param begin: начало периода
    :param end: конец периода
    :param return: ничего не возвращает
    '''
    date = begin
    stop = end
    while (date < stop):
        start = data['EVENT_TIME'].searchsorted(str(date))
        date += datetime.timedelta(days=1)
        end = data['EVENT_TIME'].searchsorted(str(date))
        drawGraphsPeriod(data, start, end, date)

def SSI(data, begin, end):
    '''
    Функция считает индекс стабильности системы за обозначенный период
    :param data: данные ЭС
    :param begin: начало периода
    :param end: конец периода
    '''
    # y - точность, y = tp/(tp+fp)
    # x = tp (true positive)

if __name__ == '__main__':
    data = pd.read_csv('2016.02.20.vyygrusska.csv', ';')

    #drawGraphsPerDay(data, datetime.datetime(2015,12,15,0,0,0), datetime.datetime(2016,01,13,0,0,0))
