import numpy as np
def calc_S(pos_x, pos_y, ball_x, ball_y):
    position = np.array([pos_x, pos_y])
    ball = np.array([ball_x, ball_y])
    return ball - position

def calc_rotation_angle(pos_x, pos_y, ball_x, ball_y):
    position = [pos_x, pos_y]
    ball = [ball_x, ball_y]
    temp = 0
    for i in range(0,len(position)):
        temp += position[i] * ball[i]
        
    
    temp2 = (np.sqrt(position[0]**2 + position[1]**2)*np.sqrt(ball[0]**2 + ball[0]**2))
    temp = temp / temp2
    return np.arccos(temp)

def point_side_check(pos_x, pos_y, ball_x, ball_y, theta):
    angle = np.arctan2(ball_y - pos_y, ball_x - pos_x) - theta
    S = calc_S(pos_x, pos_y, ball_x, ball_y)
    m = S[1]/S[0]
    c = -m*pos_x + pos_y
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

def calculate_bot_ball_angle(x, y, x2, y2, theta):
    # Calculate the angle between the bot's facing direction and the ball
    angle = np.arctan2(y2 - y, x2 - x) - theta

    # Ensure that the angle is in the range of -pi to pi
    while angle > np.pi:
        angle -= 2*np.pi
    while angle < -np.pi:
        angle += 2*np.pi

    # Determine whether the rotation should be clockwise or anti-clockwise
    if angle < -np.pi/2:
        angle += 2*np.pi
        right = 0
    elif angle > np.pi/2:
        angle -= 2*np.pi
        right = 1
    elif angle < 0:
        right = 1
    else:
        right = 0

    return round(angle,2), right    



    # end if
    
def go_to_point(pos_x, pos_y, ball_x, ball_y):
    angle = calc_rotation_angle(pos_x, pos_y, ball_x, ball_y)
    angle, right = calculate_bot_ball_angle(pos_x, pos_y, ball_x, ball_y, angle)
    return (angle, right)