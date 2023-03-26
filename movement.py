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


def stop_at_boundary(pos_x, pos_y, corner_x1, corner_y1, corner_x2, corner_y2):
    # threshold value to check for boundaries
    thresh = 10 
     
    if abs(pos_x - corner_x1) < thresh or abs(pos_x - corner_x2) < thresh or \
       abs(pos_y - corner_y1) < thresh or abs(pos_y - corner_y2) < thresh:
        
        return 1

    return 0
    

def calculate_bot_goal_angle(bot_x, bot_y, ball_x, ball_y, post_x, post_y):
    # Calculate the vectors from the bot to the ball and to the goal post
    bot_to_ball = [ball_x - bot_x, ball_y - bot_y]
    bot_to_post = [post_x - bot_x, post_y - bot_y]

    # Calculate the angle between the bot-to-ball and bot-to-post vectors using the dot product
    dot_product = bot_to_ball[0]*bot_to_post[0] + bot_to_ball[1]*bot_to_post[1]
    bot_to_ball_mag = np.sqrt(bot_to_ball[0]**2 + bot_to_ball[1]**2)
    bot_to_post_mag = np.sqrt(bot_to_post[0]**2 + bot_to_post[1]**2)
    angle = np.arccos(dot_product / (bot_to_ball_mag * bot_to_post_mag))

    # Determine whether the rotation should be clockwise or anti-clockwise using the cross product
    cross_product = bot_to_ball[0]*bot_to_post[1] - bot_to_ball[1]*bot_to_post[0]
    right = cross_product < 0

    return angle, right


def go_to_point(pos_x, pos_y, ball_x, ball_y):
    angle = calc_rotation_angle(pos_x, pos_y, ball_x, ball_y)
    angle, right = calculate_bot_ball_angle(pos_x, pos_y, ball_x, ball_y, angle)
    return [angle, right]