#https://content.u-blox.com/sites/default/files/documents/u-blox-F9-HPG-1.32_InterfaceDescription_UBX-22008968.pdf


#pip install pyubx2
#pip install pyserial

from serial import Serial
from pyubx2 import UBXReader, UBXMessage, SET, POLL
import argparse

import struct
import json

argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--serialName", help="Serial name like COM15 or ttyS0", default='COM15')
argParser.add_argument("-b", "--targetBoudrate", help="Type target boudrate", default=921600)
argParser.add_argument("-o", "--output", help="target output method UART or save to bin (BIN)", default='UART')

args = argParser.parse_args()
print(args)
serialName = args.serialName #'COM15'

def update_boudRate(old,new=921600):
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
                baudRate=new, 
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
    #print(output)
    if 'UART' in args.output:
        s = Serial(serialName, old, timeout=3)
        s.write(output)
        s.close()
    else:
        o = []
        for item in output:
            o.append(item)
        s = open("change-boudrate.txt", "w")
        s.write(json.dumps(o))
        s.close()
    

TARGET_BOUDRATE = args.targetBoudrate #921600

update_boudRate(38400,TARGET_BOUDRATE)
update_boudRate(9600,TARGET_BOUDRATE)

if 'UART' in args.output:
    stream = Serial(serialName, TARGET_BOUDRATE, timeout=3)
else:
    stream = open("setup.txt", "w")
    stream.write('[')

'''
ubr = UBXReader(stream)
(raw_data, parsed_data) = ubr.read()
print('-- Some kind of valid data is received:',parsed_data.identity, flush=True )

def poll(ubxClass, ubxID, **params):
    msg = UBXMessage(ubxClass, ubxID, POLL, **params)
    print(msg)
    output = msg.serialize()
    stream.write(output)

    while(True):
        (raw_data, parsed_data) = ubr.read()
        if ubxID in parsed_data.identity:
            print(parsed_data.identity,parsed_data, flush=True )
            return parsed_data
            break
'''

'''
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

def setup(ubxClass, ubxID, **params):
    msg = UBXMessage(ubxClass,ubxID, SET, **params)
    print(msg)
    output = msg.serialize()
    #print(output)
    if 'UART' in args.output:
        stream.write(output)
    else:
        for item in output:
            stream.write(str(item)+',')


setup(
        'CFG',
        'CFG-NAV5', 
        dyn=1, 
        minEl=1, 
        posFixMode=1, 
        drLim=1, 
        posMask=1, 
        timeMask=1, 
        staticHoldMask=1, 
        dgpsMask=1, 
        cnoThreshold=1, 
        utc=1, 
        dynModel=7, 
        fixMode=3, 
        fixedAlt=0.0, 
        fixedAltVar=1.0, 
        minElev=10, 
        drLimit=0, 
        pDop=25.0, 
        tDop=25.0, 
        pAcc=100, 
        tAcc=350, 
        staticHoldThresh=0, 
        dgnssTimeOut=60, 
        cnoThreshNumSVs=0, 
        cnoThresh=0, 
        reserved0=0, 
        staticHoldMaxDist=0, 
        utcStandard=0, 
        reserved1=0) # 

setup(
        'CFG',
        'CFG-TP5', 
        tpIdx=0, 
        version=1, 
        reserved0=0, 
        antCableDelay=50, 
        rfGroupDelay=0, 
        freqPeriod=100000, 
        freqPeriodLock=100000, 
        pulseLenRatio=10000, 
        pulseLenRatioLock=10000, 
        userConfigDelay=0, 
        active=1, 
        lockGnssFreq=1, 
        lockedOtherSet=1, 
        isFreq=0, 
        isLength=1, 
        alignToTow=1, 
        polarity=1, 
        gridUtcGnss=0, 
        syncMode=0) # setup timepulse

setup("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x00, rateDDC=0, rateUART1=0, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # NMEA-Standard GGA
setup("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x01, rateDDC=0, rateUART1=0, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # NMEA-Standard GLL
setup("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x02, rateDDC=0, rateUART1=0, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # NMEA-Standard GSA
setup("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x03, rateDDC=0, rateUART1=0, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # NMEA-Standard GSV
setup("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x04, rateDDC=0, rateUART1=0, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # NMEA-Standard RMC
setup("CFG", "CFG-MSG",msgClass=0xf0,msgID=0x05, rateDDC=0, rateUART1=0, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # NMEA-Standard VTG

setup("CFG", "CFG-MSG",msgClass=0x0a,msgID=0x09, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # UBX-MON-HW (0x0a 0x09)
setup("CFG", "CFG-MSG",msgClass=0x01,msgID=0x36, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # UBX-NAV-COV (0x01 0x36)
setup("CFG", "CFG-MSG",msgClass=0x01,msgID=0x07, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # UBX-NAV-PVT (0x01 0x07)
setup("CFG", "CFG-MSG",msgClass=0x01,msgID=0x03, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # UBX-NAV-STATUS (0x01 0x03)
setup("CFG", "CFG-MSG",msgClass=0x0d,msgID=0x03, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0) # UBX-TIM-TM2 (0x0d 0x03)

setup("CFG", "CFG-RATE", measRate=100, navRate=1, timeRef=1) # setup 10 hz rate

setup("CFG", "CFG-CFG", saveMask=b"\x1f\x1f\x00\x00", devBBR=1, devFlash=1) # save all

if 'UART' not in args.output:
    stream.write(']')

stream.close()