from ControlScripts import RotationScript, PowerMeterScript

import time


wp = RotationScript.Waveplate(0)
pm = PowerMeterScript.open_powermeter('1909737')
power = PowerMeterScript.measure(pm)
print(power)
for i in range(0,8):
    print(i)
    time.sleep(0.5)
    wp.rotate(i)
    power = PowerMeterScript.measure(pm)
    print(power)
    time.sleep(0.5)