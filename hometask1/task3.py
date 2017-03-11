"""
Задача 3.
1. Постройте ROC кривую для каждого правила.
2. Найдите коэффициент Джини для каждого правила.
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_curve, auc


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

    plt.figure()

    for i in range(1, 6):
        actual, predictions = getData(data['p' + str(i) + '_Fraud'], data['CLASS'])
        false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predictions)
        roc_auc = auc(false_positive_rate, true_positive_rate)

        plt.plot(false_positive_rate, true_positive_rate, label='%s ROC, AUC = %0.2f, Gini = %0.2f' % ('p' + str(i) + '_Fraud', roc_auc, (roc_auc * 2) - 1))

    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right', fontsize='small')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.0])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.grid(True, linestyle='-', color='0.75')
    # plt.show()

    plt.savefig('ROC-curve_with_Gini.png')