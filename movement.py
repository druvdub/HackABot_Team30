import numpy as np
def calc_S(pos_x, pos_y, ball_x, ball_y):
    position = np.array([int(pos_x), int(pos_y)])
    ball = np.array([int(ball_x), int(ball_y)])
    return [ball[0] - position[0], ball[1] - position[1]]

def calc_rotation_angle(pos_x, pos_y, ball_x, ball_y):
    position = [pos_x, pos_y]
    ball = [ball_x, ball_y]
    temp = 0
    for i in range(len(position)):
        temp += int(position[i]) * ball[i]
    temp = temp /(np.sqrt(position[0]**2 + position[1])*np.sqrt(ball[0]**2 + ball[0]**2))
    print(temp)
    return np.arccos(temp)

def calc_R(bot_angle, ball_angle):
    theta = np.abs(bot_angle - ball_angle)
    return [[np.cos(theta), -np.sin(theta)],[sin(theta), cos(theta)]]
    
def calc_number_of_angle_rotations(pos_x, pos_y, ball_x, ball_y, angle):
    return calc_rotation_angle//angle

def point_side_check(pos_x, pos_y, ball_x, ball_y):
    S = calc_S(pos_x, pos_y, ball_x, ball_y)
    temp_x = pos_x + S[0]
    temp_y = pos_y + S[1]
    m = (temp_y - pos_y)/(temp_x - pos_x)
    c = m*pos_x
    check_point = m*ball_x + c
    if (ball_y > check_point):
        if (ball_x > 0):
            return False
        else:
            return True
    else:
        if (ball_x < 0):
            return False
        else:
            return True
    # end if
    
def go_to_point(pos_x, pos_y, ball_x, ball_y):
    angle = calc_rotation_angle(pos_x, pos_y, ball_x, ball_y)
    right = point_side_check(pos_x, pos_y, ball_x, ball_y)
    return (angle, right)