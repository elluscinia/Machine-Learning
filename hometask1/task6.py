# -*- coding: utf-8 -*-
'''
6.
Создайте ансамбль в виде p = (p1_fraud + p2_fraud + p3_fraud)/3. Постройте ROC
кривую.
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc
from task5 import summ
from task3_4 import getData

def func(systems):
    return [float(summ(systems, i)) / float(3) for i,x in enumerate(systems[0])]

if __name__ == '__main__':
    data = pd.read_csv('2016.02.20.vyygrusska.csv', ';') # выгрузим данные из csv

    # функция p = (p1_fraud + p2_fraud + p3_fraud)/3
    P = func([data['p' + str(i) + '_Fraud'] for i in xrange(1, 4)])

    plt.figure()

    actual, predictions = getData(P, data['CLASS'])
    false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predictions)
    roc_auc = auc(false_positive_rate, true_positive_rate)

    plt.plot(false_positive_rate, true_positive_rate, label='%s ROC, AUC = %0.2f, Gini = %0.2f' % ('p_Fraud', roc_auc, (roc_auc * 2) - 1))

    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right', fontsize='small')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.0])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
