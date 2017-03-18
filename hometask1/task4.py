"""
Задача 4.
1. Создайте ансамбль в виде функции голосования при пороге каждого правила >=0.5,
>=0.8. Найдите необходимые пороги для каждого правила ЭС, чтобы false positive
ансамбля была минимальна.
2. Создайте ансамбль в виде p = (p1_fraud + p2_fraud + p3_fraud + p4_fraud + p5_fraud)/5. Постройте ROC
кривую.
"""
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from operator import itemgetter
from sklearn.metrics import roc_curve, auc

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
    Суммирующая вспомогательная функция для мажоритарной функции
    :param systems: решения ЭС
    :param i: номер решения ЭС
    :param return: сумма решений
    '''
    ans = 0
    for j in range(0, len(systems)):
        if systems[j][i] == 0:
            ans += -1
        else:
            ans += systems[j][i]
    return ans


def funcMajority(systems):
    '''
    Мажоритарная функция
    :param systems: ЭС и их решения
    :param return: решение функции на основании решений ЭС
    '''
    return ['F' if summ(systems, i) >= 1 else 'G' for i in range(0, len(systems[0]))]

def tnr(data, check):
    '''
    Функция для нахождения true positive rate
    :param data: решения ЭС
    :param check: проверенные данные
    :param return: tpr
    '''
    tn = len([c for d,c in zip(data, check) if (c == 'F' and d == 'F')])
    fp = len([c for d,c in zip(data, check) if (c == 'F' and d == 'G')])
    return float(tn) / float(tn+fp)


def fpr (data, check):
    '''
    Функция для нахождения false negative rate
    :param data: решения ЭС
    :param check: проверенные данные
    :param return: fnr
    '''
    return float(1) - tnr(data, check)


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def searchThresholds(data):
    '''
    Функция находит такой порог для решающего правила, чтобы FPR <= P
    :param data: данные, определённые ЭС
    :param return: минимальный fpr, набор решающих правил для каждой ЭС
    '''

    ps = itertools.permutations(list(frange(0.4, 0.9, 0.1)), 5)

    results = dict()

    for p in ps:
        majority = funcMajority([es(data['p' + str(i) + '_Fraud'], p[i-1]) for i in range(1, 6)])
        results.update({fpr(majority, data['CLASS']): p})

    minimum = sorted(results)[0]
    return minimum, results[minimum]
  

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


def func(systems):
    return [float(summ(systems, i)) / len(systems[0]) for i in range(0, len(systems[0]))]


if __name__ == '__main__':
    data = pd.read_csv('unloading.csv', ',') # выгрузим данные из csv

    p = 0.5 # задали решающее правило

    # мажоритарная функция для всех систем
    majority = funcMajority([es(data['p' + str(i) + '_Fraud'], p) for i in range(1, 6)])

    print('p =', p)

    # false positive rate для ансамбля с мажоритарной функцией
    print('false positive rate', fpr(majority, data['CLASS']))

    print('----------------------')

    p = 0.8 # задали решающее правило

    # мажоритарная функция для всех систем
    majority = funcMajority([es(data['p' + str(i) + '_Fraud'], p) for i in range(1, 6)])

    print('p =', p)

    # false positive rate для ансамбля с мажоритарной функцией
    print('false positive rate', fpr(majority, data['CLASS']))

    print('---------------------')

    fpr_min, rules = searchThresholds(data)
    print('rules for ensemble:', rules)
    print('minimum fpr:', fpr_min)


    # функция p = (p1_fraud + p2_fraud + p3_fraud + p4_fraud + p5_fraud)/5
    P = func([data['p' + str(i) + '_Fraud'] for i in range(1, 6)])

    plt.figure()

    actual, predictions = getData(P, data['CLASS'])
    false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predictions)
    roc_auc = auc(false_positive_rate, true_positive_rate)

    plt.plot(false_positive_rate, true_positive_rate, label='%s ROC, AUC = %0.2f, Gini = %0.2f' % ('p_Fraud', roc_auc, (roc_auc * 2) - 1))

    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right', fontsize='small')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.grid(True, linestyle='-', color='0.75')
    # plt.show()

    plt.savefig('ensemble_ROC-curve_with_Gini.png')
