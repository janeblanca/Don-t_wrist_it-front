import cv2
import mediapipe as mp_mediapipe
import numpy as np
import tensorflow as tf

# Load the pre-trained machine learning model
model_path = r"C:/4th_yr/Project Design 1/GRU_modelfinalest.h5"
model = tf.keras.models.load_model(model_path)

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
        # If no hands are detected, return an empty list
        return []

    return combined_landmarks

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture a frame. Exiting.")
        break

    frame_with_landmarks = draw_landmarks(frame)
    landmarks = extract_landmarks(frame)

    try:
        landmarks_arr = np.array(landmarks)

        if landmarks_arr.size > 0:  # Check if landmarks_arr is non-empty
            reshaped_landmarks = landmarks_arr.reshape((1, 1, landmarks_arr.shape[0]))

            # Make predictions using the loaded model
            predictions = model.predict(reshaped_landmarks)

            # Determine correctness for each hand
            is_right_hand_correct = predictions[0, 0] > 0.5  # Adjust the threshold as needed
            is_left_hand_correct = predictions[0, 1] > 0.5  # Adjust the threshold as needed

            # Display the text on the frame
            text_right = "Correct" if is_right_hand_correct else "Incorrect"
            text_left = "Correct" if is_left_hand_correct else "Incorrect"

            cv2.putText(frame_with_landmarks, f"Right Hand: {text_right}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if is_right_hand_correct else (0, 0, 255), 2)
            cv2.putText(frame_with_landmarks, f"Left Hand: {text_left}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if is_left_hand_correct else (0, 0, 255), 2)

            print(landmarks_arr)
            print(landmarks_arr.shape)
        else:
            print("No hand landmarks detected.")

        # Show the frame with landmarks
        cv2.imshow('Hand Landmarks', frame_with_landmarks)

    except Exception as e:
        print(f"An error occurred: {e}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

hands.close()
