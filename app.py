import cv2
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Colors and brush thickness
colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255)]
color_index = 0
brush_thickness = 15

# Create a canvas to draw
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

xp, yp = 0, 0  # Previous points

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror the image

    # Detect hand
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if lm_list:
                x1, y1 = lm_list[8]  # Tip of index finger
                x2, y2 = lm_list[12] # Tip of middle finger

                # Check fingers
                fingers = []
                if lm_list[8][1] < lm_list[6][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                if lm_list[12][1] < lm_list[10][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Selection Mode - Two fingers up
                if fingers[0] and fingers[1]:
                    xp, yp = 0, 0
                    cv2.rectangle(frame, (x1, y1-25), (x2, y2+25), colors[color_index], cv2.FILLED)
                    if y1 < 100:
                        if 0 < x1 < 320:
                            color_index = 0
                        elif 320 < x1 < 640:
                            color_index = 1
                        elif 640 < x1 < 960:
                            color_index = 2
                        elif 960 < x1 < 1280:
                            color_index = 3

                # Drawing Mode - One finger up
                elif fingers[0] and fingers[1] == 0:
                    cv2.circle(frame, (x1, y1), 15, colors[color_index], cv2.FILLED)
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    cv2.line(canvas, (xp, yp), (x1, y1), colors[color_index], brush_thickness)
                    xp, yp = x1, y1

    # Merge canvas and frame
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv_canvas = cv2.threshold(gray_canvas, 50, 255, cv2.THRESH_BINARY_INV)
    inv_canvas = cv2.cvtColor(inv_canvas, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv_canvas)
    frame = cv2.bitwise_or(frame, canvas)

    # Add color selection bar
    cv2.rectangle(frame, (0, 0), (320, 100), colors[0], cv2.FILLED)
    cv2.rectangle(frame, (320, 0), (640, 100), colors[1], cv2.FILLED)
    cv2.rectangle(frame, (640, 0), (960, 100), colors[2], cv2.FILLED)
    cv2.rectangle(frame, (960, 0), (1280, 100), colors[3], cv2.FILLED)

    cv2.imshow("Virtual Painter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
