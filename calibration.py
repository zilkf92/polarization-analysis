from ControlScripts import RotationScript, PowerMeterScript
from Settings import pm_settings
import time

serialnum = str(pm_settings.sn)
wp = RotationScript.Waveplate(0)
pm = PowerMeterScript.open_powermeter(serialnumber=serialnum)
power = PowerMeterScript.measure(pm)
print(power)
for i in range(0,8):
    print(i)
    time.sleep(0.5)
    wp.rotate(i)
    power = PowerMeterScript.measure(pm)
    print(power)
    time.sleep(0.5)