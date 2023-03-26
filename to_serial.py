import serial
import time
from scraper import scrape_test, save_data
from movement import go_to_point

PORT = "/dev/ttyUSB1"
SLEEP_TIME = 0.05

arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)

data = save_data(scrape_test())

# print(data)

r = list(data['M19'].values())

ball = list(data['B'].values())

print(r, ball)
# result = go_to_point(int(r[0]),int(r[1]),int(ball[0]),int(ball[1]))
result = go_to_point(371, 476, 839, 533)
print(result)

# combined = r+ball
# combined = combined[:5]
# combined_str = ' '.join(combined)
# print(combined_str)


def write_read_to_arduino(data):
	arduino.write(bytes(data, "utf-8"))
	time.sleep(SLEEP_TIME)
	key = arduino.readline()
	return key

# while True:

# 	data_in = f"<{combined_str}>"
# 	data_out = write_read_to_arduino(data_in)
# 	print(data_out)
