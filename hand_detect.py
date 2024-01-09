import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

mp_hands = mp.solutions.hands
try:
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
except:
    hands = None

mp_drawing = mp.solutions.drawing_utils

def extract_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    landmarks_data = []
    combined_landmarks = []
    if results.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            landmarks = []  
            for idx, landmark in enumerate(hand_landmarks.landmark):
                landmark_data = [landmark.x, landmark.y]
                if hasattr(landmark, 'z'):
                    landmark_data.append(landmark.z)
                landmarks.extend(landmark_data)
            landmarks_data.append(landmarks)
            combined_landmarks.extend(landmarks)

    return combined_landmarks

def predict_hand_action(frame):
    landmarks = extract_landmarks(frame)
    if not landmarks:
        return None

    landmarks_arr = np.array([landmarks])
    print("Landmarks shape:", landmarks_arr.shape)
    reshaped_landmarks = landmarks_arr.reshape((1, 1, landmarks_arr.shape[1]))

    predictions = model.predict(reshaped_landmarks)

    if predictions > 0.5:
        return "Correct Position"
    else:
        return "Incorrect Position"

# Load your machine learning model
model_path = r"C:\4th_yr\Project Design 1\GRU_modelfinalest.h5"
model = tf.keras.models.load_model(model_path)

# Open the camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Predict and display result
    if hands is not None:
        prediction = predict_hand_action(frame)
        if prediction:
            print(prediction)

        # Draw landmarks on the frame
        frame_with_landmarks = frame.copy()
        frame_with_landmarks = extract_landmarks(frame_with_landmarks)
        if frame_with_landmarks:
            mp_drawing.draw_landmarks(frame_with_landmarks, mp_hands.HAND_CONNECTIONS)


            cv2.imshow('Hand Landmarks', frame_with_landmarks)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if hands is not None:
    hands.close()
