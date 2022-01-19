from mindstorms import MSHub, Motor, MotorPair
import math
hub = MSHub()
wheels = MotorPair('E','A')
left_motor = Motor('A')
# coefficients
kp = 11 #proportional gain
ki = 4.2 #integral gain
kd = 92 #derivative gain  ... increase if wobbling too much
roll_target = 88.56 #balance angle  ... increase if drifting back (+0.01), decrease if drifting forward (-0.01)

# working variables
integral = 0
error = 0
start_target = 0
derivative = 0
prev_error = 0
result = 0
ks = -0.6
start = 0
start_target = 0
left_motor.set_degrees_counted(0)

hub.light_matrix.set_orientation('right')
hub.light_matrix.show('99099:99099:00000:90009:09990')  # Display a smiley face

while hub.motion_sensor.get_roll_angle()<120 and hub.motion_sensor.get_roll_angle()>60:
    error = roll_target - hub.motion_sensor.get_roll_angle()
    integral = integral + (error*0.25)
    derivative = error - prev_error
    prev_error = error
    start = (start_target - left_motor.get_degrees_counted())
    result = (error*kp) + (integral*ki) + (derivative*kd) + (start*ks)
    wheels.start_at_power(math.floor(result),0)
wheels.stop()
hub.light_matrix.show_image('ASLEEP')
