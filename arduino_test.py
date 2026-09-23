import serial
import time

arduino = serial.Serial(
    "/dev/ttyACM0",
    9600
)

time.sleep(2)

print("Turning LED ON")
arduino.write(b"1")

time.sleep(3)

print("Turning LED OFF")
arduino.write(b"0")

arduino.close()