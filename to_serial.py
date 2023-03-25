import serial
import time

PORT = '/dev/ttyUSB0'
SLEEP_TIME = 0.05

arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)

def write_read_to_arduino(data):
	arduino.write(bytes(data, "utf-8"))
	time.sleep(SLEEP_TIME)
	return arduino.readline()
n=0
while True:

	data_in = f"<Hello world!{n}>"
	data_out = write_read_to_arduino(data_in)
	print(data_out)
	n+=1
