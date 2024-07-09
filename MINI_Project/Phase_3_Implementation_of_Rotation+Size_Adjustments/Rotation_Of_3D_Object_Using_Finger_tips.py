import cv2
import mediapipe as mp
import pygame
import sys
from math import cos, sin

# Define colors
black = (0, 0, 0)  # RGB value for black
white = (255, 255, 255)  # RGB value for white

# Initialize Pygame
def initialize_pygame(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hand Gesture Controlled 3D Cube")
    return screen

# Initialize MediaPipe
def initialize_mediapipe():
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic()
    return holistic

# Draw 3D cube
def draw_3d_cube(window, angle_x, angle_y, angle_z, position):
    scale = 80
    cube_points = [
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]
    ]
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    rotation_x = [
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)]
    ]
    rotation_y = [
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)]
    ]
    rotation_z = [
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1]
    ]
    rotated_points = []
    for point in cube_points:
        rotated = point
        rotated = [sum([rotation_x[i][j] * rotated[j] for j in range(3)]) for i in range(3)]
        rotated = [sum([rotation_y[i][j] * rotated[j] for j in range(3)]) for i in range(3)]
        rotated = [sum([rotation_z[i][j] * rotated[j] for j in range(3)]) for i in range(3)]
        rotated_points.append(rotated)
    for connection in connections:
        pygame.draw.line(window, white, (rotated_points[connection[0]][0] * scale + position[0], rotated_points[connection[0]][1] * scale + position[1]),
                         (rotated_points[connection[1]][0] * scale + position[0], rotated_points[connection[1]][1] * scale + position[1]), 2)

# Check if two points are touching
def are_touching(point1, point2, threshold=30):
    distance = ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
    return distance < threshold

# Check if all given points are touching
def all_are_touching(*points, threshold=30):
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if not are_touching(points[i], points[j], threshold):
                return False
    return True

# Main function to run the program
def main():
    screen_width = 1280
    screen_height = 1024
    screen = initialize_pygame(screen_width, screen_height)
    mp_holistic = initialize_mediapipe()

    angle_x = angle_y = angle_z = 0
    rotation_speed = 0.1 # Set rotation speed

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_holistic.process(rgb_frame)

        if results.right_hand_landmarks or results.left_hand_landmarks:
            if results.right_hand_landmarks:
                right_hand_landmarks = results.right_hand_landmarks.landmark
                thumb_tip = (right_hand_landmarks[4].x * frame.shape[1], right_hand_landmarks[4].y * frame.shape[0])
                index_tip = (right_hand_landmarks[8].x * frame.shape[1], right_hand_landmarks[8].y * frame.shape[0])
                middle_tip = (right_hand_landmarks[12].x * frame.shape[1], right_hand_landmarks[12].y * frame.shape[0])
                ring_tip = (right_hand_landmarks[16].x * frame.shape[1], right_hand_landmarks[16].y * frame.shape[0])
                little_tip = (right_hand_landmarks[20].x * frame.shape[1], right_hand_landmarks[20].y * frame.shape[0])

                if are_touching(thumb_tip, index_tip):
                    angle_x += rotation_speed
                if are_touching(thumb_tip, middle_tip):
                    angle_y += rotation_speed
                if are_touching(thumb_tip, ring_tip):
                    angle_z += rotation_speed
                if are_touching(thumb_tip, little_tip):
                    angle_x -= rotation_speed
                if all_are_touching(thumb_tip, index_tip, middle_tip, ring_tip, little_tip):
                    angle_y -= rotation_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        screen.fill(black)
        draw_3d_cube(screen, angle_x, angle_y, angle_z, (screen_width // 4, screen_height // 2))  # Left side
        draw_3d_cube(screen, angle_x, angle_y, angle_z, (screen_width * 3 // 4, screen_height // 2))  # Right side
        draw_3d_cube(screen, angle_x, angle_y, angle_z, (screen_width // 2, screen_height // 4))  # Top side
        draw_3d_cube(screen, angle_x, angle_y, angle_z, (screen_width // 2, screen_height * 3 // 4))  # Bottom side
        pygame.display.update()

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
