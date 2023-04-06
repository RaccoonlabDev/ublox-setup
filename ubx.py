#https://content.u-blox.com/sites/default/files/documents/u-blox-F9-HPG-1.32_InterfaceDescription_UBX-22008968.pdf


#pip install pyubx2
#pip install pyserial

from serial import Serial
from pyubx2 import UBXReader, UBXMessage, SET, POLL

serialName = 'COM15'
'''
#Connect and set baudRate=921600s
s = Serial(serialName, 9600, timeout=3)

# CFG-PRT <UBX(CFG-PRT, portID=1, reserved0=0, enable=0, pol=0, pin=0, thres=0, charLen=3, parity=4, nStopBits=0, baudRate=921600, inUBX=1, inNMEA=1, inRTCM=0, inRTCM3=1, outUBX=1, outNMEA=1, outRTCM3=1, extendedTxTimeout=0, reserved1=0)>
msg = UBXMessage(
            'CFG',
            'CFG-PRT', 
            SET, 
            portID=1, 
            reserved0=0, 
            enable=0, 
            pol=0, 
            pin=0, 
            thres=0, 
            charLen=3, 
            parity=4, 
            nStopBits=0, 
            baudRate=921600, 
            inUBX=1, 
            inNMEA=1, 
            inRTCM=0, 
            inRTCM3=1, 
            outUBX=1, 
            outNMEA=1, 
            outRTCM3=1, 
            extendedTxTimeout=0, 
            reserved1=0)
print(msg)
output = msg.serialize()
s.write(output)
s.close()
'''

stream = Serial(serialName, 921600, timeout=3)

ubr = UBXReader(stream)






def poll(ubxClass, ubxID, **params):
    msg = UBXMessage(ubxClass, ubxID, POLL, **params)
    print(msg)
    output = msg.serialize()
    stream.write(output)

    while(True):
        (raw_data, parsed_data) = ubr.read()
        if ubxID in parsed_data.identity:
            print(parsed_data.identity,parsed_data, flush=True )
            break

poll("CFG", "CFG-PRT", portID=1)
poll("CFG", "CFG-NAV5")
poll("CFG", "CFG-TP5")
poll("CFG", "CFG-RATE")

poll("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x00) # NMEA-Standard GGA
poll("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x01) # NMEA-Standard GLL
poll("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x02) # NMEA-Standard GSA
poll("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x03) # NMEA-Standard GSV
poll("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x04) # NMEA-Standard RMC
poll("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x05) # NMEA-Standard VTG

poll("CFG", "CFG-MSG",msgClass=0x0a,msgID=0x09) # UBX-MON-HW (0x0a 0x09)
poll("CFG", "CFG-MSG",msgClass=0x01,msgID=0x36) # UBX-NAV-COV (0x01 0x36)
poll("CFG", "CFG-MSG",msgClass=0x01,msgID=0x07) # UBX-NAV-PVT (0x01 0x07)
poll("CFG", "CFG-MSG",msgClass=0x01,msgID=0x03) # UBX-NAV-STATUS (0x01 0x03)
poll("CFG", "CFG-MSG",msgClass=0x0d,msgID=0x03) # UBX-TIM-TM2 (0x0d 0x03)

'''
# UBX-MON-HW (0x0a 0x09)

'''


'''
#- UBX-NAV-COV (0x01 0x36)
msg = UBXMessage('CFG','CFG-MSG', SET, msgClass=0x01, msgID=0x36, rateUART1=0)
print(msg)
output = msg.serialize()
stream.write(output)

# save 
msg = UBXMessage("CFG","CFG-CFG", SET, saveMask=b"\x1f\x1f\x00\x00", devBBR=1, devFlash=1)
print(msg)
output = msg.serialize()
stream.write(output)
'''