import cv2
import mediapipe as mp
import math
import socket
import time

# IP address and port number of the Pico server
SERVER_IP = "192.168.218.54"
SERVER_PORT = 45000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cap = cv2.VideoCapture(0)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            thumb_tip = None
            index_tip = None
            little_tip = None

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 4:  # Thumb tip
                    thumb_tip = (cx, cy)
                    cv2.circle(img, thumb_tip, 15, (255, 0, 255), cv2.FILLED)
                elif id == 8:  # Index finger tip
                    index_tip = (cx, cy)
                    cv2.circle(img, index_tip, 15, (255, 0, 255), cv2.FILLED)
                elif id == 20:  # Little finger tip
                    little_tip = (cx, cy)
                    cv2.circle(img, little_tip, 15, (255, 0, 255), cv2.FILLED)

            if thumb_tip and index_tip:
                # Distance between thumb tip and index finger tip
                dist_thumb_index = math.sqrt(
                    (thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) / 10
                cv2.putText(img, f"1. Thumb to Index: {dist_thumb_index:.2f} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 0), 2)

            if thumb_tip and little_tip:
                # Distance between thumb tip and little finger tip
                dist_thumb_little = math.sqrt(
                    (thumb_tip[0] - little_tip[0]) ** 2 + (thumb_tip[1] - little_tip[1]) ** 2) / 10
                cv2.putText(img, f"2. Thumb to Little: {dist_thumb_little:.2f} cm", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            # Camera to hand distance estimation
            if len(results.multi_hand_landmarks) == 1:
                hand_landmarks = results.multi_hand_landmarks[0]
                x_min = min([lm.x for lm in hand_landmarks.landmark])
                x_max = max([lm.x for lm in hand_landmarks.landmark])
                y_min = min([lm.y for lm in hand_landmarks.landmark])
                y_max = max([lm.y for lm in hand_landmarks.landmark])
                box_width = x_max - x_min
                box_height = y_max - y_min
                distance = int(22.5 * 130 / (box_width *1000))
                cv2.putText(img, f"3. Distance to hand: {distance} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
            data = f"1.{dist_thumb_index},2.{dist_thumb_little},3.{distance}"
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # time.sleep(50)
            if client_socket.fileno() != -1:
                    client_socket.sendall(data.encode())

    cv2.imshow("Image", img)
    cv2.waitKey(1)
