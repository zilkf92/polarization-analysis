from ControlScripts import RotationScript, PowerMeterScript
from Settings import pm_settings
from FitFunctions import fit_functions as fit

from scipy import optimize
from math import fsum

import time
import matplotlib.pyplot as plt
import numpy as np


def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


serialnum = str(pm_settings.sn)
waveplate = RotationScript.Waveplate(0)
pm = PowerMeterScript.open_powermeter(serialnumber=serialnum)

# stores the averaged measured power for a certain angle of the waveplate
power_list = []
# stores the list of the respective angles of the waveplate
deg_list = []

# perform a sample measurement to optimize fit parameters
for alpha in np.arange(0, 180, 5):
    print(str(alpha) + " degree")
    deg_list.append(alpha)
    waveplate.rotate(alpha)
    # collect samples for averaging the value for a given angle position alpha
    power_samples = []
    count = 0
    for j in range(100):
        power_sample = PowerMeterScript.measure(pm)
        power_samples.append(power_sample)
        count = count + 1
    # calculate average power for a given angle position alpha
    average_pow = fsum(power_samples) / count
    power_list.append(average_pow)
    print(str(average_pow) + " appended")

print(power_list, deg_list)

# optimize fit parameters based on the collected sample
params, params_covariance = optimize.curve_fit(
    f=fit.sin,
    xdata=deg_list,
    ydata=power_list,
    # p0 is optional for curve_fit()
    # However, appropriate choice of initial values for sine fit is critical
    p0=[3.5e-05, (2 * np.pi) / 90, 2, 3.5e-05],
)

print(params, params_covariance)

a, b, c, d = params

plt.scatter(deg_list, power_list, label="DATA")

yvalue_list = []
xvalue_list = []
for k in np.arange(0, 360, 0.02):
    yvalue = fit.sin(x=k, a=params[0], b=params[1], c=params[2], d=params[3])
    xvalue_list.append(k)
    yvalue_list.append(yvalue)

dict = dict(zip(xvalue_list, yvalue_list))

print(dict)
print("MIN")
min = min(dict.values())
print(min)

for x, y in dict.items():
    if y == min:
        print(x)

listOfKeys = getKeysByValue(dict, min)
print("Keys with value equal to MIN")
# Iterate over the list of keys
for key in listOfKeys:
    print(key)

plt.plot(xvalue_list, yvalue_list, label="FIT", color="red")
plt.legend(loc="best")
plt.show()
