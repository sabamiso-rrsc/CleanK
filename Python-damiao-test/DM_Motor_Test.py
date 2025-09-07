import math
from DM_CAN import *
import serial
import time
import keyboard

maxTorque = 3

def MITMaxTorque(Motor, target_angle:float, kp:float):
    now_angle = Motor.getPosition()
    diff= abs(target_angle-now_angle)
    power = diff*kp
    if(power>maxTorque):
        MotorControl1.controlMIT(Motor, maxTorque/diff, 0.5, target_angle, 0,  0)
    else:
        MotorControl1.controlMIT(Motor, kp, 0.5, target_angle, 0,  0)


Motor1=Motor(DM_Motor_Type.DM4310,0x01,0x11)
Motor2=Motor(DM_Motor_Type.DM6006,0x02,0x15)
Motor3=Motor(DM_Motor_Type.DM4310,0x03,0x11)

serial_device = serial.Serial('COM7', 921600, timeout=0.5)
MotorControl1=MotorControl(serial_device)
MotorControl1.addMotor(Motor1)
MotorControl1.addMotor(Motor2)
MotorControl1.addMotor(Motor3)

if MotorControl1.switchControlMode(Motor1,Control_Type.MIT):
    print("motor1 switch MIT success")
if MotorControl1.switchControlMode(Motor2,Control_Type.MIT):
    print("motor2 switch MIT success")
if MotorControl1.switchControlMode(Motor3,Control_Type.MIT):
    print("motor3 switch MIT success")
"""
if MotorControl1.switchControlMode(Motor2,Control_Type.VEL):
    print("switch VEL success")
"""

"""
print("sub_ver:",MotorControl1.read_motor_param(Motor1,DM_variable.sub_ver))
print("Gr:",MotorControl1.read_motor_param(Motor1,DM_variable.Gr))

# if MotorControl1.change_motor_param(Motor1,DM_variable.KP_APR,54):
#     print("write success")
print("PMAX:",MotorControl1.read_motor_param(Motor1,DM_variable.PMAX))
print("MST_ID:",MotorControl1.read_motor_param(Motor1,DM_variable.MST_ID))
print("VMAX:",MotorControl1.read_motor_param(Motor1,DM_variable.VMAX))
print("TMAX:",MotorControl1.read_motor_param(Motor1,DM_variable.TMAX))

print("Motor2:")
print("PMAX:",MotorControl1.read_motor_param(Motor2,DM_variable.PMAX))
print("MST_ID:",MotorControl1.read_motor_param(Motor2,DM_variable.MST_ID))
print("VMAX:",MotorControl1.read_motor_param(Motor2,DM_variable.VMAX))
print("TMAX:",MotorControl1.read_motor_param(Motor2,DM_variable.TMAX))
"""

# MotorControl1.enable(Motor3)
MotorControl1.save_motor_param(Motor1)
MotorControl1.save_motor_param(Motor2)
MotorControl1.save_motor_param(Motor3)
MotorControl1.enable(Motor1)
MotorControl1.enable(Motor2)
MotorControl1.enable(Motor3)
i=0
time.sleep(1.5)

print("motor setup done")
MotorControl1.set_zero_position(Motor1)
MotorControl1.set_zero_position(Motor2)
MotorControl1.set_zero_position(Motor3)
time.sleep(3)
print("recording start")
data=[]
idx=0
start = time.time()
while time.time() - start < 10:
    data.append([])
    MotorControl1.controlMIT(Motor1, 0, 0, 0, 0,  0)
    MotorControl1.controlMIT(Motor2, 0, 0, 0, 0,  0)
    MotorControl1.controlMIT(Motor3, 0, 0, 0, 0,  0)
    data[idx].append(Motor1.getPosition())
    data[idx].append(Motor2.getPosition())
    data[idx].append(Motor3.getPosition())
    print(data[idx][1])

    idx+=1
    time.sleep(0.01)
print("recording stopped")


time.sleep(3)
print("moving start")
for l in data:
    print(l)
    MITMaxTorque(Motor1, l[0], 15)
    MITMaxTorque(Motor2, l[1], 15)
    MITMaxTorque(Motor3, l[2], 15)
    time.sleep(0.01)

time.sleep(5)

"""
print("start")
a=0
b=0
c=0
while True:
    if keyboard.is_pressed('w'):
        a+=1/128
    if keyboard.is_pressed('s'):
        a-=1/128
    if keyboard.is_pressed('a'):
        b+=1/64
    if keyboard.is_pressed('d'):
        b-=1/64
    if keyboard.is_pressed('left'):
        c+=1/64
    if keyboard.is_pressed('right'):
        c-=1/64
    print("a:",a,end="\t")
    print("b:",b,end="\t")
    print("c:",c)
    #MotorControl1.control_Pos_Vel(Motor1, b, 8)
    MITMaxTorque(Motor1, b, 15)
    MITMaxTorque(Motor2, a, 15)
    MITMaxTorque(Motor3, c, 15)
    MotorControl1.controlMIT(Motor1, 5, 1, b, 0,  0)
    MotorControl1.controlMIT(Motor2, 5, 1, a, 0,  0)
    MotorControl1.controlMIT(Motor3, 5, 1, c, 0,  0)
    print(Motor2.getPosition())
    time.sleep(0.01)


#语句结束关闭串口
serial_device.close()
"""