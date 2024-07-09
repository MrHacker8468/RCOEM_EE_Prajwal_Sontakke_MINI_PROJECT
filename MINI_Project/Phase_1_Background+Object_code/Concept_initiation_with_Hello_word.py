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

# Create a font object
def create_font(font_size):
    return pygame.font.Font(None, font_size)

# Render text on a surface
def render_text(text, font, color):
    return font.render(text, True, color)

# Draw the 'X' shape
def draw_x(screen, screen_width, screen_height, scale_size):
    pygame.draw.line(screen, white, (0, 0), (screen_width, screen_height), 2 * scale_size)
    pygame.draw.line(screen, white, (screen_width, 0), (0, screen_height), 2 * scale_size)

# Draw text on a panel with rotation
def draw_text(screen, text_surface, position, angle):
    rotated_text = pygame.transform.rotate(text_surface, angle)
    text_rect = rotated_text.get_rect(center=position)
    screen.blit(rotated_text, text_rect.topleft)

# Main function to run the program
def main():
    screen_width = 1920
    screen_height = 1080
    scale_size = 1  # 100% scale
    screen = initialize_pygame(screen_width, screen_height)

    font_size = int(86)
    font = create_font(font_size)
    text_surface = render_text("HELLO, WORLD!", font, blue)

    panel_width = screen_width // 3
    panel_height = screen_height // 3

    panel_positions = {
        "top": (panel_width, 0),
        "left": (0, panel_height),
        "right": (panel_width * 2, panel_height),
        "bottom": (panel_width, panel_height * 2)
    }

    text_positions = {
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
            draw_text(screen, text_surface, text_positions[panel], -90 if panel == "left" else 90 if panel == "right" else 180 if panel == "top" else 0)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
