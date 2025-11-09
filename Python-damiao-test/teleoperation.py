import math
from DM_CAN import *
import serial
import time
import keyboard


maxTorque = 10.0

def MITMaxTorque(MCC :MotorControl, Motor, target_angle:float, kp:float, target_vel:float, kd:float):
    now_angle = Motor.getPosition()
    diff= abs(target_angle-now_angle)
    power = diff*kp
    if(power>maxTorque):
        MCC.controlMIT(Motor, maxTorque/diff, kd, target_angle, target_vel,  0)
    else:
        MCC.controlMIT(Motor, kp, kd, target_angle, target_vel,  0)


K_p = 20

Motor1=Motor(DM_Motor_Type.DM6006,0x01,0x15)
Motor2=Motor(DM_Motor_Type.DM6006,0x02,0x15)
Motor3=Motor(DM_Motor_Type.DM4310,0x03,0x11)
Motor4=Motor(DM_Motor_Type.DM4310,0x04,0x11)
Motor5=Motor(DM_Motor_Type.DM4310,0x05,0x11)

Motor2_1=Motor(DM_Motor_Type.DM6006,0x01,0x15)
Motor2_2=Motor(DM_Motor_Type.DM6006,0x02,0x15)
Motor2_3=Motor(DM_Motor_Type.DM4310,0x03,0x11)
Motor2_4=Motor(DM_Motor_Type.DM4310,0x04,0x11)
Motor2_5=Motor(DM_Motor_Type.DM4310,0x05,0x11)

motorlist = [Motor1,Motor2,Motor3,Motor4,Motor5]
motorlist2 = [Motor2_1,Motor2_2,Motor2_3,Motor2_4,Motor2_5]

serial_device = serial.Serial('COM6', 921600, timeout=0.5)          #follower arm DM
serial_device2 = serial.Serial('COM7', 921600, timeout=0.5)         #follower arm STS
serial_device3 = serial.Serial('COM5', 921600, timeout=0.5)         #leader arm DM
serial_device4 = serial.Serial('COM9', 921600, timeout=0.5)         #leader arm STS
MotorControl1=MotorControl(serial_device)
MotorControl2=MotorControl(serial_device2)  #STS motors
MotorControl3=MotorControl(serial_device3)
MotorControl4=MotorControl(serial_device4)  #for reading STS motors


for i in range(5):
    MotorControl1.addMotor(motorlist[i])

for i in range(5):
    MotorControl3.addMotor(motorlist2[i])

controllerid = 0x0f

motorid = 1
motorid2 = 2

for i in range(5):
    if MotorControl1.switchControlMode(motorlist[i],Control_Type.MIT):
        print("1st arm motor"+str(i)+" switch MIT success")
    
for i in range(5):
    if MotorControl3.switchControlMode(motorlist2[i],Control_Type.MIT):
        print("2nd arm motor"+str(i)+" switch MIT success")



for i in range(5):
    MotorControl1.save_motor_param(motorlist[i])
    MotorControl1.enable(motorlist[i])
    MotorControl1.set_zero_position(motorlist[i])
for i in range(5):
    MotorControl3.save_motor_param(motorlist[i])
    MotorControl3.enable(motorlist[i])
    MotorControl3.set_zero_position(motorlist[i])


i=0
time.sleep(1.5)

print("motor setup done")
#time.sleep(3)
#MotorControl1.controlMIT(Motor, maxTorque/diff, kd, target_angle, target_vel,  0)
for i in range(5):
    MotorControl1.controlMIT(motorlist[i], 0, 0, 0, 0,  0)
print("tele-operation start")

data=[]
idx=0
start = time.time()
#while time.time() - start < 10:
while keyboard.is_pressed('s')==False:
    l=[]
    MotorControl4.STSControl_read(controllerid, motorid)
    for i in range(5):
        MotorControl3.controlMIT(motorlist[i], 0, 0, 0, 0,  0)

    time.sleep(0.005)
    
    for i in range(5):
        l.append(motorlist2[i].getPosition())
    MotorControl4.STSControl_read(controllerid, motorid2)
    l.append(MotorControl4.sts_map[motorid])
    MotorControl2.STSControl_write(controllerid, motorid, l[5])
    
    l.append( MotorControl4.sts_map[motorid2])
    for i in range(5):
        MITMaxTorque(MotorControl1, motorlist[i], l[i], K_p, 0, 1)
    MotorControl2.STSControl_write(controllerid, motorid2, l[6])
    
    print([float(q) for q in l])

    #data.append(l)
    idx+=1
    time.sleep(0.005)
