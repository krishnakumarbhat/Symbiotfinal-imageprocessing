import socket
import network
import machine

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
addr = socket.getaddrinfo('0.0.0.0', 45000)[0][-1] # Get the IP address of the server and port number to bind socket to
s = socket.socket()         # Create a socket object
s.bind(addr)                # Bind the socket object to the IP address and port number
s.listen(1)                 # Listen for incoming connections
print('listening on', addr)

while True:
    client_socket, client_address = s.accept()
    print("Incoming connection from", client_address)

    # Receive data from client (your laptop)
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Received data:", data)

        # Split data into three values
        values = data.decode().split(",")

        # Print values to console
        for value in values:
            print("Received value:", value)

    # Close client socket
    client_socket.close()

