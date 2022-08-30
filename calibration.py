from tokenize import Double
from ControlScripts import RotationScript, PowerMeterScript
from Settings import pm_settings
from scipy.optimize import curve_fit

import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def fit_function(x, a, b, c, d):
    return a * np.sin(b * x + c) + d

serialnum = str(pm_settings.sn)
wp = RotationScript.Waveplate(0)
pm = PowerMeterScript.open_powermeter(serialnumber=serialnum)
power = PowerMeterScript.measure(pm)
power_list = []
deg_list = []

for i in range(0,4):
    j = float(i)
    deg_list.append(j)
    time.sleep(0.5)
    wp.rotate(i)
    power = PowerMeterScript.measure(pm)
    print(power)
    power_list.append(power)
    time.sleep(0.5)

print(power_list, deg_list)

popt, pcov = curve_fit(fit_function, deg_list, power_list)
print(popt, pcov)

a, b, c, d = popt

y_line = []
for i in deg_list:
    y = fit_function(i, a, b, c, d)
    y_line.append(y)

plt.scatter(deg_list, power_list)
plt.plot(deg_list, y_line)
plt.show()