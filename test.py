import serial
import time

arduino = serial.Serial(port='COM4',  baudrate=9600, timeout=.1)

def write_read(x):
    arduino.write(bytes('aaa',  'utf-8'))
    time.sleep(0.05)
    data = arduino.readline().decode()
    return  data


while True:
    num = ''
    value  = write_read(num)
    print(value)
