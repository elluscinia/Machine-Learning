# -*- coding: utf-8 -*-
'''
8.
Выполните п.3-6, изменив степень полинома. Что будет при степени 2, 3, при степени
5, 6, 7? Как изменился результат?
'''
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = pd.read_csv('regression_x_y.2.csv', ';')
    x = data['X']
    y = data['Y']

    best_vals = np.polyfit(x=x, y=y, deg=6)

    polynomial = np.poly1d(best_vals)

    plt.figure()
    plt.plot(x, y, 'ro')
    plt.plot(x, polynomial(x))

    plt.ylabel('Y')
    plt.xlabel('X')
    plt.show()
