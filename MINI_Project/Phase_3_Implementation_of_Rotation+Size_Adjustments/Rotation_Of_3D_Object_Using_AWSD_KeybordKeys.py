import pygame
import sys
from math import cos, sin

# Initialize Pygame
def initialize_pygame(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hologram Display")
    return screen

# Define colors
black = (0, 0, 0)  # RGB value for black
light_blue = (0, 255, 255)
 # RGB value for white

# Draw 3D cube
def draw_3d_cube(window, angle_x, angle_y, angle_z, position):
    scale = 50
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
        pygame.draw.line(window, light_blue, (rotated_points[connection[0]][0] * scale + position[0], rotated_points[connection[0]][1] * scale + position[1]),
                         (rotated_points[connection[1]][0] * scale + position[0], rotated_points[connection[1]][1] * scale + position[1]), 2)

# Main function to run the program
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
    rotation_speed = 0.002  # Set rotation speed

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

        screen.fill(black)
        draw_3d_cube(screen, angle_x_top, angle_y_top, angle_z_top, (screen_width // 2, screen_height // 4))  # Top cube
        draw_3d_cube(screen, angle_x_bottom, angle_y_bottom, angle_z_bottom, (screen_width // 2, screen_height * 3 // 4))  # Bottom cube
        draw_3d_cube(screen, angle_x_left, angle_y_left, angle_z_left, (screen_width // 4, screen_height // 2))  # Left cube
        draw_3d_cube(screen, angle_x_right, angle_y_right, angle_z_right, (screen_width * 3 // 4, screen_height // 2))  # Right cube
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
