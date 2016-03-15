# -*- coding: utf-8 -*-
'''
2.
Придумайте способ удалить выбросы. Напишите функцию удаления выбросов и
сохраните результат в файл regression_x_y.2.csv. Постройте график по точкам.
'''
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

def polynom(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e


if __name__ == '__main__':
    data = pd.read_csv('regression_x_y.csv', ';')
    x = data['X']
    y = data['Y']
    summ = 0
    for i in y:
        summ += i
    avY = summ/len(y)

    summ2 = 0
    for i in y:
        summ2 += (i - avY)**2

    sigma = np.sqrt(summ2/len(y)) # среднестатистическое отклонение

    newY = []
    newX = []
    for i in xrange(1, len(y)):
        if abs(y[i] - y[i-1]) < sigma/2:
            newY.append(y[i])
            newX.append(x[i])

    raw_data = {'X': newX, 'Y': newY}
    df = pd.DataFrame(raw_data, columns = ['X', 'Y'])
    df.to_csv('regression_x_y.2.csv', index=False, sep = ';')

    data = pd.read_csv('regression_x_y.2.csv', ';')
    x = data['X']
    y = data['Y']

    best_vals, covar = curve_fit(polynom, x, y)

    plt.figure()
    plt.plot(x, y, 'ro')
    plt.plot(x, polynom(x, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4]))

    plt.ylabel('Y')
    plt.xlabel('X')
    plt.show()

    # best_vals, covar = curve_fit(polynom, x, y)

    # как вариант
    #best_vals = np.polyfit(x=x, y=y, deg=4)

    # Ys = polynom(x, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4])

    # plt.figure()
    # plt.plot(newX, newY, 'ro')
    #
    # plt.ylabel('Y')
    # plt.xlabel('X')
    # plt.show()
