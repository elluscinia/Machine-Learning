"""
Задача 1.
1. Напишите функцию, строящую на плоскости точки от двух переменных (Xi, Xj) Сами
Xi и Xj подаются на вход системы.
2. Проанализируйте всевозможные комбинации признаков. (Каково их количество,
кстати?)
Выберете 2-3 наиболее характерных пары признаков и сохраните их в *.jpg файлах.
"""

'''
X2 - дата + время (перевести в числовой формат)
X3 - uid или hash
X4 - uid или hash
X5 - uid или hash
X6 - uid или hash
X9 - числовые поля
X10 - числовые поля
X11 - ОС (задать в соответствии с ОС цифру)
X12 - валюта (задать в соответствии с валютой цифру)
X13 - числовые поля
X14 - числовые поля
X15 - числовые поля
X16 - браузер (задать в соответствии с браузером цифру)
X17 - числовые поля
X18 - числовые поля
X22 - числовые поля
X23 - IP - адрес
X24 - город (использовать код города)
X26 - вид поля не установлен

'''

import sys
import csv
import datetime
import itertools

import matplotlib.pyplot as plt


def update_dict(set_dict):
    '''
    Присвоение элементам списка числовых обозначений
    '''
    return_dict = dict()
    for i, st in enumerate(set_dict):
        return_dict.update({st: i})
    return return_dict

if __name__ == '__main__':
    data = list()

    for row in csv.reader(open('unloading.csv'), delimiter=';'):
        data.append(row[0].split(','))

    data = data[1:].copy()

    '''
     0 EVENT_TIME - ok
     1 USER_HASH 
     2 EVENT_TYPE 
     3 EVENT_TYPE_EX 
     4 AMOUNT - ok
     5 X2 - ok
     6 X3 
     7 X4 
     8 X5 
     9 X6 
     10 X9 - ok
     11 X10 - ok
     12 X11 - ok
     13 X12 - ok
     14 X13 - ok
     15 X14 - ok
     16 X15 - ok
     17 X16 - ok
     18 X17 - ok
     19 X18 - ok
     20 X22 - ok
     21 X23 
     22 X24 - ok
     23 X26 
     24 COOKIE 
     25 p1_Fraud 
     26 p2_Fraud 
     27 p3_Fraud 
     28 p4_Fraud 
     29 CLASS
    '''

    # приведём поля EVENT_TIME и X2 в удобный для отображения на графиках формат
    for date in data:
        # EVENT_TIME
        dt = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
        date[0] = dt.timestamp()

        # X2
        dt = datetime.datetime.strptime(date[5], "%Y-%m-%d %H:%M:%S")
        date[5] = dt.timestamp()


    os_dict = update_dict(set([d[12] for d in data])) # словарь соответствия ОС числовым обозначения

    for d in data:
        d[12] = os_dict.get(d[12])


    currency_dict = update_dict(set([d[13] for d in data])) # словарь соответствия валюты числовым обозначениям

    for d in data:
        d[13] = currency_dict.get(d[13])


    browsers_dict = update_dict(set([d[17] for d in data])) # словарь соответствия браузера числовым обозначениям

    for d in data:
        d[17] = currency_dict.get(d[17])


    cities_dict = update_dict(set([d[22] for d in data])) # словарь соответствия браузера числовым обозначениям

    for d in data:
        d[22] = cities_dict.get(d[22])


    characteristics_set = [0, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22]

    characteristics_description = {
                                  0:'EVENT_TIME',
                                  4:'AMOUNT',
                                  5:'X2',
                                  10:'X9',
                                  11:'X10',
                                  12:'X11',
                                  13:'X12',
                                  14:'X13',
                                  15:'X14',
                                  16:'X15',
                                  17:'X16',
                                  18:'X17',
                                  19:'X18',
                                  20:'X22',
                                  22:'X24',
    }

    # комбинации характеристик
    characteristics_combinations = itertools.combinations(characteristics_set, 2)

    values = ['', 'NULL', 'empty'] # список неопределённых значений

    for combination in characteristics_combinations:
        x = [float(d[combination[0]]) if d[combination[0]] not in values and type(d[combination[0]])!=type(None) else 0 for d in data]
        y = [float(d[combination[1]]) if d[combination[1]] not in values and type(d[combination[1]])!=type(None) else 0 for d in data ]

        plt.title("Зависимость " + characteristics_description.get(combination[1]) + " от " + characteristics_description.get(combination[0]))
        plt.xlabel(characteristics_description.get(combination[0]))
        plt.ylabel(characteristics_description.get(combination[1]))


        plt.scatter(x, y)
        plt.autoscale(tight=True)
        plt.grid(True, linestyle='-', color='0.75')
        # plt.show()
        plt.savefig(characteristics_description.get(combination[1]) + '(' + characteristics_description.get(combination[0]) + ').png')
