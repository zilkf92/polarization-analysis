from ThorLabsDriver.RotationMount import open_serial, move_abs
from Settings import mount_settings, port_settings


class Waveplate:
    '''
    Class for high level operations on the waveplate which is mounted in the
    respective Thorlabs motor
    '''
    
    def __init__(self, address):
        '''
        Initializes the motors

        Parameters
        ----------
        address :   Integer value referring to the bus address
        offset  :   Float value referring to offset of waveplate in
                    absolute degrees
        '''
        self.address = address
        self.offset = mount_settings.offset[address]

    def rotate(self, angle):
        '''
        Rotates the Rotation Mount

        Parameters
        ---------
        angle : Float value specifying the target position of the Rotation Mount
                in absolute degrees
        '''
        bus = open_serial(port_settings.comport, timeout=10)
        move_abs(bus, self.address, angle + self.offset)
        bus.close()
