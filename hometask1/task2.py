# -*- coding: utf-8 -*-
'''
1.
Для каждой ЭС найдите порог решающего правила, для которого false positive не
более 0.2
'''

# перебираем решающее правило от 0 до 1,
# пока false positive rate не станет менее или равно 0.2

from task1 import *

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
    while x < y:
        x += jump
        falsepositive = fpr(data, check, x)
        if falsepositive <= p:
            return x

if __name__ == '__main__':
    falsepositive = 0.2
    data = pd.read_csv('2016.02.20.vyygrusska.csv', ';') # выгрузим данные из csv

    for i in xrange(1, 4):
        print 'p' + str(i) + '_Fraud System'

        print 'false positive rate threshold'
        print searchThreshold(data['p' + str(i) + '_Fraud'], data['CLASS'], falsepositive)

        print '-------------------------------------------'
