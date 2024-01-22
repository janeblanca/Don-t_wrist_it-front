import cv2
import mediapipe as mp

class HandLandmarksDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    # def draw_landmarks(self, frame):
    #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     results = self.mp_hands.process(frame_rgb)
    #
    #     if results.multi_hand_landmarks:
    #         for hand_landmarks in results.multi_hand_landmarks:
    #             self.mp_drawing.draw_landmarks(
    #                 frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
    #             )
    #     return frame

    def draw_landmarks(self, frame):
        results = self.process_frame(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )
        return frame

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

    # def detect_hand_landmarks(self):
    #     cap = cv2.VideoCapture(0)
    #
    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if not ret:
    #             break
    #
    #         frame_with_landmarks = self.draw_landmarks(frame)
    #         landmarks = self.extract_landmarks(frame)
    #
    #         landmarks_arr = np.array(landmarks)
    #         reshaped_landmarks = landmarks_arr.reshape((1, 1, landmarks_arr.shape[0]))
    #
    #         print(landmarks_arr)
    #         print(landmarks_arr.shape)
    #         # Show the frame with landmarks
    #         cv2.imshow('', frame_with_landmarks)
    #
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     self.hands.close()

if __name__ == "__main__":
    detector = HandLandmarksDetector()
    # Use detector methods as needed
    # When done, release resources using detector.release_resources()
    # detector.detect_hand_landmarks()
