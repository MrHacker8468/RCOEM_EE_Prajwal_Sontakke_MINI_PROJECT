import cv2
import mediapipe as mp
import pyautogui

def main():
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic()

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands
        results = holistic.process(rgb_frame)

        if results.right_hand_landmarks or results.left_hand_landmarks:
            # Right hand landmarks
            if results.right_hand_landmarks:
                right_hand_landmarks = results.right_hand_landmarks.landmark
                for landmark in right_hand_landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                # Get the positions of thumb, index, middle, ring, and little fingers
                thumb_tip = (right_hand_landmarks[4].x * frame.shape[1], right_hand_landmarks[4].y * frame.shape[0])
                index_tip = (right_hand_landmarks[8].x * frame.shape[1], right_hand_landmarks[8].y * frame.shape[0])
                middle_tip = (right_hand_landmarks[12].x * frame.shape[1], right_hand_landmarks[12].y * frame.shape[0])
                ring_tip = (right_hand_landmarks[16].x * frame.shape[1], right_hand_landmarks[16].y * frame.shape[0])
                little_tip = (right_hand_landmarks[20].x * frame.shape[1], right_hand_landmarks[20].y * frame.shape[0])

                # Check finger touches and simulate key presses
                if are_touching(thumb_tip, index_tip):
                    pyautogui.press('a')
                if are_touching(thumb_tip, middle_tip):
                    pyautogui.press('w')
                if are_touching(thumb_tip, ring_tip):
                    pyautogui.press('d')
                if are_touching(thumb_tip, little_tip):
                    pyautogui.press('s')
                if all_are_touching(thumb_tip, index_tip, middle_tip, ring_tip, little_tip):
                    pyautogui.press('wd')

            # Left hand landmarks
            if results.left_hand_landmarks:
                left_hand_landmarks = results.left_hand_landmarks.landmark
                for landmark in left_hand_landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Display the resulting frame
        cv2.imshow('Hand Detection', frame)

        # Exit when 'Esc' is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release the capture and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def are_touching(point1, point2, threshold=30):
    """
    Check if two points are touching, given a threshold.
    """
    distance = ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
    return distance < threshold

def all_are_touching(*points, threshold=30):
    """
    Check if all given points are touching, given a threshold.
    """
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if not are_touching(points[i], points[j], threshold):
                return False
    return True

if __name__ == "__main__":
    main()
