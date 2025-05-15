import cv2
import numpy as np
import mediapipe as mp
import time

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Colors and brush thickness
color_palette = [
    (255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255),
    (255, 255, 0), (0, 165, 255), (128, 0, 128), (0, 0, 0)  # Last one is eraser (black)
]
color_index = 0
brush_thickness = 15
eraser_thickness = 50
brush_types = ['Normal', 'Spray', 'Calligraphy']
brush_type_index = 0

# Create a canvas to draw
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

xp, yp = 0, 0  # Previous points
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror the image
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Draw color palette
    for i, color in enumerate(color_palette):
        x1, x2 = i * 160, (i + 1) * 160
        cv2.rectangle(frame, (x1, 0), (x2, 100), color, cv2.FILLED)
        if color == (0, 0, 0):
            cv2.putText(frame, "Eraser", (x1 + 30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if lm_list:
                x1, y1 = lm_list[8]   # Tip of index finger
                x2, y2 = lm_list[12]  # Tip of middle finger

                # Finger status detection
                fingers = []
                fingers.append(1 if lm_list[8][1] < lm_list[6][1] else 0)
                fingers.append(1 if lm_list[12][1] < lm_list[10][1] else 0)
                fingers.append(1 if lm_list[16][1] < lm_list[14][1] else 0)
                fingers.append(1 if lm_list[20][1] < lm_list[18][1] else 0)
                fingers.append(1 if lm_list[4][0] > lm_list[2][0] else 0)  # Thumb

                # --- Clear canvas ---
                if fingers == [1, 1, 1, 1, 1]:
                    canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
                    cv2.putText(frame, "Canvas Cleared", (450, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)

                # --- Change brush type ---
                elif fingers == [1, 1, 1, 0, 0]:
                    brush_type_index = (brush_type_index + 1) % len(brush_types)
                    cv2.putText(frame, f"Brush: {brush_types[brush_type_index]}", (900, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
                    time.sleep(0.5)  # prevent rapid toggling

                # --- Color Selection Mode (2 fingers) ---
                elif fingers[0] and fingers[1]:
                    xp, yp = 0, 0
                    cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), color_palette[color_index], cv2.FILLED)
                    if y1 < 100:
                        color_index = x1 // 160

                # --- Drawing Mode (only index finger up) ---
                elif fingers[0] and not fingers[1]:
                    cv2.circle(frame, (x1, y1), 15, color_palette[color_index], cv2.FILLED)
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    current_color = color_palette[color_index]
                    if current_color == (0, 0, 0):  # Eraser
                        cv2.line(canvas, (xp, yp), (x1, y1), (0, 0, 0), eraser_thickness)
                    else:
                        if brush_types[brush_type_index] == 'Normal':
                            cv2.line(canvas, (xp, yp), (x1, y1), current_color, brush_thickness)
                        elif brush_types[brush_type_index] == 'Spray':
                            for _ in range(20):
                                offset_x = np.random.randint(-10, 10)
                                offset_y = np.random.randint(-10, 10)
                                cv2.circle(canvas, (x1 + offset_x, y1 + offset_y), 1, current_color, -1)
                        elif brush_types[brush_type_index] == 'Calligraphy':
                            cv2.ellipse(canvas, (x1, y1), (20, 5), 0, 0, 360, current_color, -1)

                    xp, yp = x1, y1

    # Merge canvas and frame
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv_canvas = cv2.threshold(gray_canvas, 50, 255, cv2.THRESH_BINARY_INV)
    inv_canvas = cv2.cvtColor(inv_canvas, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv_canvas)
    frame = cv2.bitwise_or(frame, canvas)

    # Display FPS and brush
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time)) if (curr_time - prev_time) != 0 else 0
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {fps}', (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, f'Brush: {brush_types[brush_type_index]}', (10, 650), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow("Virtual Painter", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):
        cv2.imwrite("my_virtual_painting.png", canvas)
        print("Drawing saved as 'my_virtual_painting.png'")

cap.release()
cv2.destroyAllWindows()
