from ControlScripts import RotationScript, PowerMeterScript
from Settings import pm_settings
from FitFunctions import fit_functions as fit

from scipy import optimize
from math import fsum

import time
import matplotlib.pyplot as plt
import numpy as np

serialnum = str(pm_settings.sn)
waveplate = RotationScript.Waveplate(0)
pm = PowerMeterScript.open_powermeter(serialnumber=serialnum)

power_list = []
deg_list = []

for i in np.arange(0, 180, 5):
    print(str(i) + " degree")
    deg_list.append(i)
    waveplate.rotate(i)
    power_samples = []
    count = 0
    for j in range(100):
        power_sample = PowerMeterScript.measure(pm)
        power_samples.append(power_sample)
        count = count + 1
    average_pow = fsum(power_samples) / count
    power_list.append(average_pow)
    print(str(average_pow) + " appended")

print(power_list, deg_list)

params, params_covariance = optimize.curve_fit(
    f=fit.sin, xdata=deg_list, ydata=power_list
)
print(params, params_covariance)

a, b, c, d = params

plt.scatter(deg_list, power_list, label="DATA")

yvalue_list = []
for k in range(len(deg_list)):
    yvalue = fit.sin(x=deg_list[k], a=params[0], b=params[1], c=params[2], d=params[3])
    print(yvalue)
    yvalue_list.append(yvalue)

print(yvalue_list)

plt.plot(deg_list, yvalue_list, label="FIT", color="red")
plt.legend(loc="best")
plt.show()
