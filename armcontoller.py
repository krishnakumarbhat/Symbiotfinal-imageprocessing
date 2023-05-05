import socket
import network
import machine
from machine import Pin, PWM
import utime

# Define mapping for servo motor
# v1 mapped to 2 > 11 and less
# v2 mapped to 5 values between 2 to 34
# v3 mapped to 3 values between 22 to 221
v1_min, v1_max = 2, 11
v2_min, v2_max = 2, 34
v3_min, v3_max = 22, 221

# Define duty cycle limits for servo motor
min_duty = 1200000
max_duty = 2000000
MIN1 = 1200000
MAX1 = 2000000
MIN2 = 1450000
MAX2 = 400000
MIN3 = 2000000
MAX3 = 400000

pwm1 = PWM(Pin(0))
pwm1.freq(50)
pwm1.duty_ns(MIN1)
pwm2 = PWM(Pin(1))
pwm2.freq(50)
pwm2.duty_ns(MIN2)
pwm3 = PWM(Pin(2))
pwm3.freq(50)
pwm3.duty_ns(MIN3)

# Connect to WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Asdf", "abcd1234")

while not wifi.isconnected():
    pass

# Print IP address once connected
print("Connected to WiFi")
print("IP address:", wifi.ifconfig()[0])

# Set up server socket
addr = socket.getaddrinfo('0.0.0.0', 47150)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
    client_socket, client_address = s.accept()
    print("Incoming connection from", client_address)

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # Split data into three values
        values = data.decode().strip().split(",")[:3]
        
        # Print values to console
        #for value in values:
            #print("Received value:", value)
        
        # Convert values to floats
        try:
            #v1, v2, v3 = [float(val) for val in values]
            v1, v2, v3 = [float(val.split('.')[1]) for val in values]
            print(f"v1: {v1},v2: {v2},v3:{v3} ")
            
        except ValueError:
            print("Invalid data format")
            continue
        
        if 0<v1 < 11.26:
            pwm1.duty_ns(MIN1)
            utime.sleep(1.65)
        elif 11.26<v1 :
            pwm1.duty_ns(MAX1)
            utime.sleep(1.65)
        
        # Map v1 to duty cycle range and set PWM


    # Map v2 to duty cycle range and set PWM
        if 0<v2 < 13:
            pwm2.duty_ns(int(MAX2/5))
        elif 8.5 < v2 < 15:
            pwm2.duty_ns(int(2*MAX2/5))
        elif 15 < v2 < 21.5:
            pwm2.duty_ns(int(3*MAX2/5))
        elif 21.5 < v2 < 28:
            pwm2.duty_ns(int(4*MAX2/5))
        elif 28<v2:
            pwm2.duty_ns(MAX2)
        utime.sleep(1.65)

    # Map v3 to duty cycle range and set PWM
        if 0 < v3 < 63:
            pwm3.duty_ns(int(MAX3/3))
        elif 63 < v3 < 126:
            pwm3.duty_ns(int(2*MAX3/3))
        elif 126 < v3:
            pwm3.duty_ns(MAX3)
        utime.sleep(1.65)

    # Close client socket
        client_socket.close()


