import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up constants
CELL_WIDTH = 10  # Width of each cell
CELL_HEIGHT = 10  # Height of each cell
GRID_COLS = 63  # Number of columns
GRID_ROWS = 47  # Number of rows
SCREEN_WIDTH = CELL_WIDTH * GRID_COLS * 2 + 2  # Double the width for side-by-side display plus 2px for the border
SCREEN_HEIGHT = CELL_HEIGHT * GRID_ROWS

# Directories containing the images
DIR1 = 'design1'
DIR2 = 'design2'

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Cursor Image Display')

# Set up font for displaying text
font = pygame.font.SysFont(None, 36)
caption_font = pygame.font.SysFont(None, 16, bold=True)  # Caption font, bold, 16px

# Create a custom cursor
cursor_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.circle(cursor_surface, (0, 255, 0), (10, 10), 10, 1)  # Green border, no fill
cursor = pygame.cursors.Cursor((10, 10), cursor_surface)
pygame.mouse.set_cursor(cursor)

def get_cell_image(directory, x, y):
    """Load image based on cell coordinates from a specific directory."""
    file_name = f"{(y + 1) * CELL_HEIGHT}_{(x + 1) * CELL_WIDTH}.png"
    try:
        return pygame.image.load(os.path.join(directory, file_name))
    except FileNotFoundError:
        # Handle missing images or invalid paths
        return None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Calculate cell coordinates
    cell_x = mouse_x // CELL_WIDTH
    cell_y = mouse_y // CELL_HEIGHT
    
    # Determine if the mouse is in the left or right half of the screen
    half = 'left' if mouse_x < (SCREEN_WIDTH - 2) // 2 else 'right'
    
    # Adjust cell_x for the right half
    if half == 'right':
        cell_x = max(0, (mouse_x - (SCREEN_WIDTH // 2 + 1))) // CELL_WIDTH
    
    # Load the corresponding images from both directories
    image1 = get_cell_image(DIR1, cell_x, cell_y)
    image2 = get_cell_image(DIR2, cell_x, cell_y)
    
    # Clear screen
    screen.fill((255, 255, 255))
    
    # Draw the images if they exist, else display coordinates
    if image1:
        screen.blit(image1, (0, 0))
        # Add caption
        caption_surface = caption_font.render("Design1", True, (255, 0, 0))
        screen.blit(caption_surface, (5, 5))
    else:
        # Render text for the left side
        text_surface = font.render(f"({cell_x}, {cell_y})", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
        screen.blit(text_surface, text_rect)
        # Add caption
        caption_surface = caption_font.render("Design1", True, (255, 0, 0))
        screen.blit(caption_surface, (5, 5))
    
    # Draw the border
    pygame.draw.line(screen, (0, 0, 0), ((SCREEN_WIDTH // 2 - 1), 0), ((SCREEN_WIDTH // 2 - 1), SCREEN_HEIGHT), 2)
    
    if image2:
        screen.blit(image2, ((SCREEN_WIDTH // 2) + 1, 0))
        # Add caption
        caption_surface = caption_font.render("Design2", True, (255, 0, 0))
        screen.blit(caption_surface, ((SCREEN_WIDTH // 2) + 6, 5))
    else:
        # Render text for the right side
        text_surface = font.render(f"({cell_x}, {cell_y})", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
        screen.blit(text_surface, text_rect)
        # Add caption
        caption_surface = caption_font.render("Design2", True, (255, 0, 0))
        screen.blit(caption_surface, ((SCREEN_WIDTH // 2) + 6, 5))
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
