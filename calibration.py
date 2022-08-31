from ControlScripts import RotationScript, PowerMeterScript
from Settings import pm_settings
from scipy.optimize import curve_fit
from math import fsum

import time
import matplotlib.pyplot as plt
import numpy as np

serialnum = str(pm_settings.sn)
waveplate = RotationScript.Waveplate(0)
pm = PowerMeterScript.open_powermeter(serialnumber=serialnum)

power_list = []
deg_list = []

for i in np.arange(0, 180, 1):
    deg_list.append(i)
    time.sleep(0.5)
    waveplate.rotate(i)
    power_samples = []
    count = 0
    for j in range(100):
        power_sample = PowerMeterScript.measure(pm)
        power_samples.append(power_sample)
        count = count + 1
    average_pow = fsum(power_samples)/count
    power_list.append(average_pow)
    time.sleep(0.5)

print(power_list, deg_list)

plt.scatter(deg_list, power_list)
plt.show()