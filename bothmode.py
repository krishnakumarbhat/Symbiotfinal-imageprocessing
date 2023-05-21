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
addr = socket.getaddrinfo('0.0.0.0', 47675)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

button_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
i=0

while True:
    if button_pin.value() == 0:
        print("inside")
        a= [7,4,1,2,0,4,6,2,1]
        while i<9:
            v1 ,v2,v3 = a[i],a[i],a[i]
            i+=1
            print(i)
            print(v1,v2,v3)
            
            if v1 ==0 :
                pwm1.duty_ns(MAX1)

            elif v1==1 :
                pwm1.duty_ns(MIN1)
            utime.sleep(0.65)
            
            if v2 == 2 or v2 == 3:
                pwm2.duty_ns(MIN2)
            elif v2 ==4:
                pwm2.duty_ns(MAX2)
            utime.sleep(0.65)
            
            if  v3 == 5 or v3 == 6:
                pwm3.duty_ns(MIN3)
            elif v3== 7:
                pwm3.duty_ns(MAX3)
            utime.sleep(0.65)
    client_socket, client_address = s.accept()
    print("Incoming connection from", client_address)

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # Split data into three values
        #values = data.decode().strip().split(",")[:3]
        
        # Print values to console
        #for value in values:
            #print("Received value:", value)
        
        # Convert values to floats
        #try:
            #v1, v2, v3 = [float(val) for val in values]
            #v1, v2, v3 = [float(val.split('.')[1]) for val in values]
            #print(f"v1: {v1},v2: {v2},v3:{v3} ")
        values = data.decode().strip().split(",")[:3]
        try:
            v1, v2, v3 = [float(val) for val in values]
            print(f"v1: {v1}, v2: {v2}, v3: {v3}")
            #print(values)
            
        except ValueError:
            print("Invalid data format")
            continue
        print(v1,v2,v3)
            
        if v1 ==0 :
            pwm1.duty_ns(MAX1)

        elif v1==1 :
            pwm1.duty_ns(MIN1)
        utime.sleep(0.65)
            
        if v2 == 2 or v2 == 3:
            pwm2.duty_ns(MIN2)
        elif v2 ==4:
            pwm2.duty_ns(MAX2)
        utime.sleep(0.65)
            
        if  v3 == 5 or v3 == 6:
            pwm3.duty_ns(MIN3)
        elif v3== 7:
            pwm3.duty_ns(MAX3)
        utime.sleep(0.65)
        

    # Close client socket
    client_socket.close()
