# -*- coding: utf-8 -*-
'''
6.
Байесовский подход. Аналогично п.5 перебором из 10000 различных вариантов
найдите 1-10% наиболее подходящих функций. Постройте эти функции методом:
plt.plot(X, [func_reg(x) for x in X], 'b-', alpha=0.05, linewidth=4). Возможно
разумно задать другие alpha и linewidth?
'''

import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt, pi, exp

if __name__ == '__main__':
    main()
