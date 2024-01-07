import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def draw_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return frame

def extract_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    landmarks_data = []
    if results.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            landmarks = {}
            for idx, landmark in enumerate(hand_landmarks.landmark):
                landmark_name = {
                    0: 'wrist',
                    1: 'thumb_cmc',
                    2: 'thumb_mcp',
                    3: 'thumb_ip',
                    4: 'thumb_tip',
                    5: 'index_finger_mcp',
                    6: 'index_finger_pip',
                    7: 'index_finger_dip',
                    8: 'index_finger_tip',
                    9: 'middle_finger_mcp',
                    10: 'middle_finger_pip',
                    11: 'middle_finger_dip',
                    12: 'middle_finger_tip',
                    13: 'ring_finger_mcp',
                    14: 'ring_finger_pip',
                    15: 'ring_finger_dip',
                    16: 'ring_finger_tip',
                    17: 'pinky_mcp',
                    18: 'pinky_pip',
                    19: 'pinky_dip',
                    20: 'pink_tip'
                }.get(idx, f"landmark_{idx}")
                landmarks[f'hand_{hand_idx}_{landmark_name}'] = {
                    'X': landmark.x,
                    'Y': landmark.y,
                    'Z': landmark.z if hasattr(landmark, 'z') else None
                }
            landmarks_data.append(landmarks)
    return landmarks_data

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_with_landmarks = draw_landmarks(frame)
    landmarks = extract_landmarks(frame)

    landmarks_arr = np.array([list(l.values()) for l in landmarks])
    reshaped_landmarks = np.expand_dims(landmarks_arr, axis=1)
    print(landmarks_arr)
    print(landmarks_arr.shape)
    # Show the frame with landmarks
    cv2.imshow('Hand Landmarks', frame_with_landmarks)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

hands.close()
