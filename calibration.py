from ControlScripts import RotationScript, PowerMeterScript
from Settings import pm_settings
from FitFunctions import fit_functions as fit

from scipy import optimize
from math import fsum

import time
import matplotlib.pyplot as plt
import numpy as np

# this function returns keys from dict for given values
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


# power meter and rotation mount initialization
serialnum = str(pm_settings.sn)
waveplate = RotationScript.Waveplate(0)
pm = PowerMeterScript.open_powermeter(serialnumber=serialnum)

# stores the averaged measured power for a certain angle of the waveplate
power_list = []
# stores the list of the respective angles of the waveplate
deg_list = []

# perform a sample measurement to optimize fit parameters
for alpha in np.arange(0, 180, 10):
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

pa, pb, pc, pd = params

# x_data needs to be array-like or scalar to prevent TypeError in return value from sin function
x_data = np.arange(start=0, stop=360, step=0.005, dtype=np.longdouble)
y_data = np.array(object=[], dtype=np.longdouble)

for x in x_data:
    y = fit.sin(x=x, a=pa, b=pb, c=pc, d=pd)
    y_data = np.append(arr=y_data, values=y)

minval = min(y_data)
dict = dict(zip(x_data, y_data))
print("Minimum Angle:")
print(getKeysByValue(dict, minval))

plt.figure(figsize=(10, 8), dpi=80)

plt.scatter(deg_list, power_list, label="DATA")
plt.plot(
    x_data,
    fit.sin(x=x_data, a=pa, b=pb, c=pc, d=pd),
    label="Fitted function",
    color="red",
)

plt.tight_layout()
plt.legend(loc="best")
plt.show()
