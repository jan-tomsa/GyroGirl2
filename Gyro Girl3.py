from mindstorms import MSHub, Motor, MotorPair
from mindstorms import ColorSensor
import math
import time
from time import ticks_add, ticks_diff

# Initialize color sensor
cl_sens = ColorSensor('C')

hub = MSHub()
wheels = MotorPair('E','A')
left_motor = Motor('A')
# coefficients
kp = 11 #proportional gain
ki = 4.2 #integral gain
kd = 92 #derivative gain  ... increase if wobbling too much

#RT_STRAIGHT = 88.56 
RT_STRAIGHT = 88.55 #balance angle... increase if drifting back (+0.01), decrease if drifting forward (-0.01)
#RT_BACKWARD = 85
RT_BACKWARD = 85.5
RT_FORWARD = 90
roll_target = RT_STRAIGHT

# working variables
integral = 0
error = 0
start_target = 0
derivative = 0
prev_error = 0
result = 0
ks = -0.6
start = 0
left_motor.set_degrees_counted(0)

hub.light_matrix.set_orientation('right')
hub.light_matrix.show('99099:99099:00000:90009:09990')  # Display a smiley face

# Prepare for printing the inital roll angle
roll_angle_printed = False

# Allow grace period in which roll angle is not tested (it may be confused rigth after start)
grace_period = ticks_add(time.ticks_ms(), 200)

counter = 0

while (hub.motion_sensor.get_roll_angle()<120 and hub.motion_sensor.get_roll_angle()>60) or (ticks_diff(grace_period, time.ticks_ms()) > 0):
    roll_angle = hub.motion_sensor.get_roll_angle()
    error = roll_target - roll_angle
    integral = integral + (error*0.25)
    derivative = error - prev_error
    prev_error = error
    deg_counted = left_motor.get_degrees_counted()
    start = (start_target - deg_counted)
    result = (error*kp) + (integral*ki) + (derivative*kd) + (start*ks)
    wheels.start_at_power(math.floor(result),0)

    # Print roll angle only once
    #if (not roll_angle_printed):
    #if (counter < 10):
    #    print("# ",counter," ra: ", roll_angle, " dc:", deg_counted)
    #    roll_angle_printed = True

    if (counter == 400):
        roll_target = RT_BACKWARD
        hub.light_matrix.show('00900:09090:90009:00900:00900')# Display up arrow

    if (counter == 600):
        roll_target = RT_STRAIGHT
        hub.light_matrix.show('99999:90009:90009:90009:99999')# Display square


    if (counter == 800):
        roll_target = RT_FORWARD
        hub.light_matrix.show('00900:00900:90009:09090:00900')# Display down arrow

    if (counter == 1200):
        roll_target = RT_STRAIGHT
        hub.light_matrix.show('90009:09090:00900:09090:90009')# Display x


    # Process light sensor
    reflect = cl_sens.get_reflected_light()
    if reflect > 60:
        hub.status_light.on('blue')
        #roll_target = RT_BACKWARD
        #hub.light_matrix.show('00900:09090:90009:00900:00900')# Display up arrow
    else:
        hub.status_light.on('red')

    counter = counter + 1

wheels.stop()
hub.light_matrix.show_image('ASLEEP')
