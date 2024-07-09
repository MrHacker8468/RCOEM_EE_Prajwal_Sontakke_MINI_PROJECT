import pygame
import sys
import cv2
import mediapipe as mp
import math
from math import cos, sin

# Initialize Pygame
def initialize_pygame(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hologram Display")
    return screen

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

black = (0, 0, 0)  # RGB value for black
light_blue = (0, 255, 255)

# OpenCV setup
cap = cv2.VideoCapture(0)  # You can change the argument to a video file if needed

# Main function to run the program
def main():
    screen_width = 1024
    screen_height = 1024
    screen = initialize_pygame(screen_width, screen_height)

    running = True
    angle_x_top = angle_y_top = angle_z_top = 0
    angle_x_bottom = angle_y_bottom = angle_z_bottom = 0
    angle_x_left = angle_y_left = angle_z_left = 0
    angle_x_right = angle_y_right = angle_z_right = 0
    rotation_speed = 0.01  # Set rotation speed
    scale_factor = 80  # Initial scale factor

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        # Reset angles if 'R' key is pressed
        if keys[pygame.K_r]:
            angle_x_top = angle_y_top = angle_z_top = 0
            angle_x_bottom = angle_y_bottom = angle_z_bottom = 0
            angle_x_left = angle_y_left = angle_z_left = 0
            angle_x_right = angle_y_right = angle_z_right = 0

        # Handle rotation for each cube according to key presses
        if keys[pygame.K_a]:
            angle_y_top += rotation_speed
            angle_y_bottom -= rotation_speed
            angle_x_left += rotation_speed
            angle_x_right -= rotation_speed

        if keys[pygame.K_d]:
            angle_y_top -= rotation_speed
            angle_y_bottom += rotation_speed
            angle_x_left -= rotation_speed
            angle_x_right += rotation_speed

        if keys[pygame.K_w]:
            angle_x_top += rotation_speed
            angle_x_bottom += rotation_speed
            angle_y_left += rotation_speed
            angle_y_right += rotation_speed

        if keys[pygame.K_s]:
            angle_x_top -= rotation_speed
            angle_x_bottom -= rotation_speed
            angle_y_left -= rotation_speed
            angle_y_right -= rotation_speed

        # Read frame from the video stream
        ret, frame = cap.read()
        if ret:
            # Convert the image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect hands
            results = hands.process(rgb_frame)

            # If hands are detected
            # If hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Check if it's the left hand
                    hand_index = results.multi_hand_landmarks.index(hand_landmarks)
                    if results.multi_handedness[hand_index].classification[0].label == "Left":
                        # Get the coordinates of thumb tip and index finger tip
                        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        thumb_tip_x, thumb_tip_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
                        index_finger_tip_x, index_finger_tip_y = int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0])

                        # Calculate the distance between thumb tip and index finger tip
                        distance = math.sqrt((thumb_tip_x - index_finger_tip_x) ** 2 + (thumb_tip_y - index_finger_tip_y) ** 2)
                        
                        # Update scale factor based on distance
                        scale_factor = distance / 1.25 # Adjust as needed
                    else:
                        # If it's not the left hand, reset scale factor
                        scale_factor = 80  # Reset scale factor
            else:
                # If no hands are detected, reset scale factor
                scale_factor = 80  # Reset scale factor

        screen.fill(black)
        draw_3d_cube(screen, angle_x_top, angle_y_top, angle_z_top, (screen_width // 2, screen_height // 4), scale_factor)  # Top cube
        draw_3d_cube(screen, angle_x_bottom, angle_y_bottom, angle_z_bottom, (screen_width // 2, screen_height * 3 // 4), scale_factor)  # Bottom cube
        draw_3d_cube(screen, angle_x_left, angle_y_left, angle_z_left, (screen_width // 4, screen_height // 2), scale_factor)  # Left cube
        draw_3d_cube(screen, angle_x_right, angle_y_right, angle_z_right, (screen_width * 3 // 4, screen_height // 2), scale_factor)  # Right cube
        pygame.display.update()

    # Clean up
    cap.release()
    pygame.quit()
    sys.exit()

# Draw 3D cube
def draw_3d_cube(window, angle_x, angle_y, angle_z, position, scale):
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
        rotated = [sum([rotation_x[i][j] * point[j] for j in range(3)]) for i in range(3)]
        rotated = [sum([rotation_y[i][j] * rotated[j] for j in range(3)]) for i in range(3)]
        rotated = [sum([rotation_z[i][j] * rotated[j] for j in range(3)]) for i in range(3)]
        rotated_points.append(rotated)
    
    # Draw connections between the points
    for connection in connections:
        pygame.draw.line(window, light_blue, 
                         (rotated_points[connection[0]][0] * scale + position[0], rotated_points[connection[0]][1] * scale + position[1]),
                         (rotated_points[connection[1]][0] * scale + position[0], rotated_points[connection[1]][1] * scale + position[1]), 2)

if __name__ == "__main__":
    main()
