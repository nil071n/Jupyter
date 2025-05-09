import pygame
import math
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
NUM_DOTS = 200
MAX_RADIUS = 300
MAX_Z = 500
TRAIL_LENGTH = 20
FPS = 60  # Frames per second for smooth animation
SPEED = 0.02

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Rotating Galaxy")
clock = pygame.time.Clock()

# Particle setup with 3D positions (x, y, z)
particles = []
for i in range(NUM_DOTS):
    speed = random.uniform(0.01, 0.05)
    radius = random.uniform(50, MAX_RADIUS)
    size = random.randint(2, 5)
    z = random.uniform(1, MAX_Z)
    hue_shift = random.uniform(0, 360)
    particles.append({
        "angle": random.uniform(0, 2 * math.pi),
        "speed": speed,
        "radius": radius,
        "size": size,
        "z": z,  # Depth in 3D space
        "trail": [],
        "hue_shift": hue_shift
    })

# HSL to RGB conversion for vibrant colors
def hsl_to_rgb(h, s, l):
    from colorsys import hls_to_rgb
    r, g, b = hls_to_rgb(h / 360, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))

# Perspective projection function
def project_3d_to_2d(x, y, z, focal_length=500):
    # Perspective projection formula
    factor = focal_length / (focal_length + z)
    x_2d = x * factor + CENTER_X
    y_2d = y * factor + CENTER_Y
    return int(x_2d), int(y_2d)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill background with black

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw particles with 3D rotation
    for p in particles:
        # Update the angle for 3D rotation (rotate around y-axis)
        p["angle"] += p["speed"]
        p["z"] -= 1  # Move the particle forward in 3D space
        if p["z"] < 1:  # Reset the particle to the back once it's too close
            p["z"] = MAX_Z

        # 3D to 2D conversion (for the visual effect)
        x = p["radius"] * math.cos(p["angle"])
        y = p["radius"] * math.sin(p["angle"])
        
        # Apply perspective projection (simulate depth)
        x_2d, y_2d = project_3d_to_2d(x, y, p["z"])

        # Update trail
        p["trail"].append((x_2d, y_2d))
        if len(p["trail"]) > TRAIL_LENGTH:
            p["trail"].pop(0)

        # Draw the trail with fading effect
        for i, (tx, ty) in enumerate(p["trail"]):
            opacity = i / TRAIL_LENGTH  # Fading effect
            color = hsl_to_rgb((p["hue_shift"] + i * 10) % 360, 1, 0.5)
            pygame.draw.circle(screen, color, (tx, ty), p["size"])

    pygame.display.flip()
    clock.tick(FPS)  # Control the frame rate

pygame.quit() 
