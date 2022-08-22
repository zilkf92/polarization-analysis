from WaveplateControl.RotationScript import Waveplate
import time


wp = Waveplate(0)

for i in range(0,359):
    print(i)
    time.sleep(5)
    wp.rotate(i)