import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM14', 9600)  # Update to your actual COM port
time.sleep(2)  # Wait for Arduino to initialize

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Function to detect which fingers are open
def get_finger_array(hand_landmarks):
    """
    Returns a list representing the state of each finger:
    1 = Open, 0 = Closed
    Order: [Thumb, Index, Middle, Ring, Pinky]
    """
    finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    fingers = []

    # ✅ Thumb: corrected logic (open → 1 → 180°, closed → 0 → 0°)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(0)  # Thumb closed
    else:
        fingers.append(1)  # Thumb open

    # ✅ Other fingers (Index to Pinky)
    for i in range(1, 5):
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_tips[i] - 2].y:
            fingers.append(1)  # Finger open
        else:
            fingers.append(0)  # Finger closed

    return fingers

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for selfie view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_array = get_finger_array(hand_landmarks)

            # Send data to Arduino
            data_to_send = "".join(map(str, finger_array)) + "\n"
            arduino.write(data_to_send.encode())
            print(f"Sent: {data_to_send.strip()}")

            # Display on screen
            cv2.putText(frame, f"Fingers: {finger_array}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()