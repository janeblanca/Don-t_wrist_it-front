import cv2
import mediapipe as mp

class HandLandmarksDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def extract_landmarks(self, frame):
        results = self.process_frame(frame)
        combined_landmarks = []

        if results.multi_hand_landmarks:
            num_hands = min(2, len(results.multi_hand_landmarks))

            for hand_idx in range(num_hands):
                landmarks = []
                hand_landmarks = results.multi_hand_landmarks[hand_idx]
                for landmark in hand_landmarks.landmark:
                    landmark_data = [landmark.x, landmark.y]
                    if hasattr(landmark, 'z'):
                        landmark_data.append(landmark.z)
                    landmarks.extend(landmark_data)
                combined_landmarks.extend(landmarks)

        return combined_landmarks

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.mp_hands.process(frame_rgb)

    def release_resources(self):
        self.mp_hands.close()


if __name__ == "__main__":
    detector = HandLandmarksDetector()
