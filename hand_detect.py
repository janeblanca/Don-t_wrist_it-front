import cv2
import mediapipe as mp_mediapipe
import numpy as np

mp_hands = mp_mediapipe.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp_mediapipe.solutions.drawing_utils

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
        num_hands = min(2, len(results.multi_hand_landmarks))
        combined_landmarks = []
        for hand_idx in range(num_hands):
            landmarks = []  # Initialize landmarks for each hand separately
            hand_landmarks = results.multi_hand_landmarks[hand_idx]
            for idx, landmark in enumerate(hand_landmarks.landmark):
                landmark_data = [landmark.x, landmark.y]
                if hasattr(landmark, 'z'):
                    landmark_data.append(landmark.z)
                landmarks.extend(landmark_data)
            landmarks_data.append(landmarks)
            combined_landmarks.extend(landmarks)
    else:
        # If no hands are detected, return an empty list or handle it as needed
        combined_landmarks = []

    return combined_landmarks

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_with_landmarks = draw_landmarks(frame)
    landmarks = extract_landmarks(frame)

    landmarks_arr = np.array(landmarks)
    reshaped_landmarks = landmarks_arr.reshape((1, 1, landmarks_arr.shape[0]))

    # Uncomment the following lines when you have the model for predictions
    # predictions = model.predict(reshaped_landmarks)

    print(landmarks_arr)
    print(landmarks_arr.shape)
    # Show the frame with landmarks
    cv2.imshow('Hand Landmarks', frame_with_landmarks)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

hands.close()
