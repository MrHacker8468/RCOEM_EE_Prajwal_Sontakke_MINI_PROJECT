import pygame
import sys

# Initialize Pygame
def initialize_pygame(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hologram Display")
    return screen

# Define colors
black = (0, 0, 0)  # RGB value for black
white = (255, 255, 255)  # RGB value for white
blue = (0, 0, 255)  # RGB value for blue

# Draw the 'X' shape
def draw_x(screen, screen_width, screen_height, scale_size):
    pygame.draw.line(screen, white, (0, 0), (screen_width, screen_height), 2 * scale_size)
    pygame.draw.line(screen, white, (screen_width, 0), (0, screen_height), 2 * scale_size)

# Draw squares on panels
def draw_square(screen, position, size):
    square_rect = pygame.Rect(position[0] - size // 2, position[1] - size // 2, size, size)
    pygame.draw.rect(screen, blue, square_rect)

# Main function to run the program
def main():
    screen_width = 1920
    screen_height = 1080
    scale_size = 1  # 100% scale
    square_size = 150  # Size of the square

    screen = initialize_pygame(screen_width, screen_height)

    panel_width = screen_width // 3
    panel_height = screen_height // 3

    panel_positions = {
        "top": (panel_width + panel_width // 2, panel_height // 2),
        "left": (panel_width // 2, panel_height + panel_height // 2),
        "right": (panel_width * 2 + panel_width // 2, panel_height + panel_height // 2),
        "bottom": (panel_width + panel_width // 2, panel_height * 2 + panel_height // 2)
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(black)
        draw_x(screen, screen_width, screen_height, scale_size)

        for panel, pos in panel_positions.items():
            draw_square(screen, pos, square_size)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
