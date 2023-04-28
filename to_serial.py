import serial
import time
from scraper import scrape_test
from movement import go_to_point, stop_at_boundary, check_if_ball_is_near, calculate_bot_goal_angle

PORT = "COM6"
SLEEP_TIME = 0.05

arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)

check_for_goal_sides = True

# g42 when ours is left side, g43 - right side
our_goal = list()

# data = save_data(scrape_test())

# print(data)

# r = list(data['M19'].values())

# ball = list(data['B'].values())

# print(r, ball)
# result = go_to_point(int(r[0]),int(r[1]),int(ball[0]),int(ball[1]))
# result = go_to_point(371, 476, 839, 533)
# print(result)

# combined = r+ball
# combined = combined[:5]
# combined_str = ' '.join(combined)
# print(combined_str)

def fetch_data():
	global check_for_goal_sides, our_goal
	data = scrape_test()
	g42 = list(data['G42'].values())
	g43 = list(data['G43'].values())
	c0 = list(data['C0'].values())
	c1 = list(data['C1'].values())
	ball = list(data['B'].values())
	r = list(data['M20'].values())
	dbot = list(data['M19'].values())



	# print(ball)
	# print(r)
	# print(c0)
	# print(c1)

	if check_for_goal_sides:
		# It means that the bot is on the right side
		if (int(g42[0]) + int(g43[0]))//2 <= int(c0[0]):
			our_goal = g43
		else:
			our_goal = g42

		check_for_goal_sides = False 
	
	result = go_to_point(int(r[0]),int(r[1]),int(ball[0]),int(ball[1]))
	result = check_if_ball_is_near(result, int(ball[0]),int(ball[1]),int(our_goal[0]),int(our_goal[1]))
	
	at_boundary = stop_at_boundary(int(r[0]), int(r[1]), int(c0[0]), int(c0[1]), int(c1[0]), int(c1[1]))

	defenderbot = calculate_bot_goal_angle(int(dbot[0]), int(dbot[1]),int(ball[0]),int(ball[1]), int(our_goal[0]), int(our_goal[1]))
	def_boundary = stop_at_boundary(int(dbot[0]), int(dbot[1]), int(c0[0]), int(c0[1]), int(c1[0]), int(c1[1]))
	result.append(at_boundary)
	result.extend(defenderbot)
	result.append(def_boundary)
	result = tuple(result)
	return result


def write_read_to_arduino(data):
	arduino.write(bytes(data, "utf-8"))
	time.sleep(SLEEP_TIME)
	key = arduino.readline()
	return key


while True:
	combined = fetch_data()

	combined_str = ' '.join(str(i) for i in combined)
	# print(combined_str)
	data_in = f"<{combined_str}>"
	data_out = write_read_to_arduino(data_in)
	# print(data_out)
